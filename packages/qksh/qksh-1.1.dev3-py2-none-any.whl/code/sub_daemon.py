from daemon import runner
import BaseHTTPServer
import StringIO
import thread
import time
import pickle
import requests
import ihealth_api
import logging
import sys

session_cookie = StringIO.StringIO()
session_cookie.write(None)

# save cookie validation result in poker
poker = StringIO.StringIO()
poker.write(None)

# username/password
secret = StringIO.StringIO()
secret.write(None)


# TODO: need to move to logging system
def logging_config():

    logger = logging.getLogger("sub_daemon")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler("qksh.log")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(name)s: %(''message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return fh


def _update_cookie():

    logger = logging.getLogger("sub_daemon")

    # unpickle credential cache
    user_pass_list = pickle.loads(secret.getvalue())
    username = user_pass_list[0]
    password = user_pass_list[1]

    logger.info('updating cookie in cache. running get_cookie()')
    # logger.info('username: %s, password; %s', username, password)

    cookie = ihealth_api.RetrieveCookie.get_cookie(username, password)
    session_cookie.truncate(0)
    pickle.dump([requests.utils.dict_from_cookiejar(cookie[0]),
                 cookie[1]], session_cookie)
    logger.info('session cookie cache updated.')


def wrapper_request_handler():

    """
    implement decorator of class here, handling GET / POST request
    """

    logger = logging.getLogger("sub_daemon")

    class HttpRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

        def do_HEAD(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            self.send_response(200)

            # return cached credential
            if self.path == '/auth.do':
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(secret.getvalue())
                logger.info('sending cached credential')
                return

            if self.path == '/poke':
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(poker.getvalue())
                logger.info('sending poke response.')
                return

            # return cached session cookie
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if session_cookie.getvalue() != '':
                logger.debug('sending session cookie %s',
                             session_cookie.getvalue())
                self.wfile.write(session_cookie.getvalue())
            else:
                self.wfile.write("No session cookie found!")
                logger.info('No session cookie found!')

        # read hlen bytes of data and write to file-like string buffer. flush
        # session_cookie every time received a POST request and break the loop
        def do_POST(self):

            if self.path == '/auth.do':

                logger.info('receiving credential.')

                hlen = self.headers.get('Content-Length')
                secret.truncate(0)
                secret.write(
                    self.rfile.read(int(hlen)))
                logger.info('credential updated.')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # logger.info('update credential in cache. %s',
                #             self.rfile.read(int(hlen)))
                # logger.info('credential updated.')
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # look for content-length header, saving hlen bytes into memory
                # and update poker with 'valid' value.
                for i in self.headers:
                    if i == 'content-length':
                        hlen = self.headers.get('Content-Length')
                        ret = self.rfile.read(int(hlen))
                        session_cookie.truncate(0)
                        session_cookie.write(ret)
                        poker.write('valid')
                        logger.info('saving session cookie in memory cache.')
                        logger.debug('session cookie value: %s',
                                     session_cookie.getvalue())

    return HttpRequestHandler


class Credential:

    def __init__(self):

        requests.packages.urllib3.disable_warnings()

        self.logger = logging.getLogger("sub_daemon")

        # TODO: temporary disable stdout/stderr, not sure how to redirect
        # stdout when called by subprocess and logging to qksh.log file.
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = '/var/run/credential.pid'
        self.pidfile_timeout = 5

    def restful_loopback_server(
            self,
            server_class=BaseHTTPServer.HTTPServer,
            handler_class=BaseHTTPServer.BaseHTTPRequestHandler):

        # Restful server socket will handle GET/POST request from qksh.
        # Lookback server is hardcoded running on port 63333. Each HTTP request
        # will be dispatched to handler_class

        host = "127.0.0.1"
        port = 63333
        server_address = (host, port)

        self.logger.info('binding restful_loopback_server to 127.0.0.1:63333.')
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()

    def timeout_checker(self):

        # periodically validate session cookie at an interval of 10 mins,
        # if approaching deadline, refresh cookie as needed.
        file_link = 'https://ihealth.f5.com/qkview-analyzer/'

        while 1:
            counter = 0
            while counter <= 4:
                if session_cookie.getvalue() is not '':
                    cookie = pickle.loads(session_cookie.getvalue())

                    self.logger.info('downloading test page.')
                    ret = requests.get(file_link, verify=False,
                                       cookies=cookie[0])

                    # if Location header is in the response, invoke
                    # update_cookie function, otherwise, touch poker with
                    # 'valid' value
                    if 'Location' in ret.headers.keys():
                        self.logger.info(
                            'Location header found in response,'
                            'invoke _update_cookie()')
                        _update_cookie()
                    else:
                        self.logger.info('no Location header found in '
                                         'response.')

                        # convert epoch time to system time for easy reading.
                        t_epoch = cookie[1].split(':')[1].strip('}')
                        expr_time = time.strftime(
                            '%Y-%m-%d %H:%M:%S',
                            time.localtime(float(t_epoch)))
                        poker.truncate(0)
                        poker.write('valid')
                        self.logger.info(
                            'session cookie expire at %s, status: valid',
                            expr_time)
                counter += 1
                time.sleep(600)

            # session cookie need to be updated every 50 mins.
            self.logger.info(
                'session cookie about to expire, calling _update_cookie()')
            _update_cookie()

    def run(self):

        # daemonize the loopback server
        thread.start_new_thread(self.timeout_checker, ())

        handler_class = wrapper_request_handler()
        self.restful_loopback_server(handler_class=handler_class)


def daemon_run():

    fh = logging_config()
    logger = logging.getLogger("sub_daemon")

    if sys.argv[1] == 'start':
        logger.info('sub_daemon initializing...')

    # TODO: how to handle the situation where daemon is running while pid
    # file is deleted for whatever reason.
    credential = Credential()
    daemon_runner = runner.DaemonRunner(credential)
    try:
        # This ensures that the logger file handle does not get closed
        # during daemonization
        daemon_runner.daemon_context.files_preserve = [fh.stream]
        daemon_runner.do_action()

        if sys.argv[1] == 'stop':
            logger.info('Terminating on signal 15, sub_daemon stopped.')

    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    daemon_run()
