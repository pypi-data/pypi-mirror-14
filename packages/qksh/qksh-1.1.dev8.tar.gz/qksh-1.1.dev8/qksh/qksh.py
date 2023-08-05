#!/bin/bash/env python
from ihealth_api import RetrieveCookie
import toggle_sub_daemon
import re
import os
import requests
import StringIO
import pickle
import getpass
import logging
import sys


logger = logging.getLogger('ihealth_api.qksh')


def _get_sub_daemon_path():

    return re.sub(
        'toggle_sub_daemon\.py.*', 'sub_daemon.py', toggle_sub_daemon.__file__)

toggle = toggle_sub_daemon.ToggleDaemon(_get_sub_daemon_path())


def _parse_arg(arg_list=None, ):

    ptn_case = re.compile(r'^(c\d{7}|1-\d{8,10})$', re.IGNORECASE)
    ptn_url = re.compile(r"""^https://ihealth\.f5\.com/qkview-analyzer/qv
                                 (/\d{7}) # regex match qkview id
                                 (/commands|/files) # reg match commands/files
                                 (/view|/download) # reg match view/download
                                 (/\w*) #regex match hash value""",
                         re.IGNORECASE | re.X)

    # if no argv supplied to qksh, call usage, or split the first argument
    # and do regex check

    logger.info('Checking arguments, argument list: %s',
                str(arg_list[1:]).strip('[]'))

    if len(arg_list) > 1:

        logger.info('parsing arguments list.')

        if sys.argv[1] == 'status':
            m, n = toggle.status_daemon()
            logger.info('daemon status: %s, pid: %s ', m, n)
            if m == 0:
                print 'pid file exists, sub_daemon is running, PID: ', n
            if m == 1:
                print 'pid file exists, sub_daemon is not running.'
            if m == 2:
                print 'pid file does not exists, sub_daemon is running', n
            if m == 3:
                print 'pid file does not exists, sub_daemon is not running'
            sys.exit(0)
        if sys.argv[1] == 'start':
            toggle.start_daemon()
            print 'sub_daemon started.'
            sys.exit(0)
        if sys.argv[1] == 'stop':
            toggle.stop_daemon()
            print 'sub_daemon stopped.'
            sys.exit(0)
        if sys.argv[1] == 'restart' or sys.argv[1] == 'reload':
            toggle.restart_daemon()
            print 'sub_daemon', sys.argv[1]
            sys.exit(0)
        if sys.argv[1] == 'forceload':
            toggle.forceload_daemon()
            print 'sub_daemon forceloaded.'
            sys.exit(0)

        splited_url = arg_list[1].split('/')
        case_num_match = ptn_case.match(sys.argv[1])
        url_match = ptn_url.match(sys.argv[1])

        # return 1:
        #     first arg is case number
        # return 2:
        #     first arg is url and it's a file downloading link
        # return 3:
        #     first arg is url and it's a commands downloading link
        if case_num_match is not None:
            return 1
        elif url_match is not None:
            if splited_url[6] == 'files':
                return 2
            if splited_url[6] == 'commands':
                return 3
        else:
            usage()
            sys.exit(1)
    else:
        usage()
        sys.exit(1)


# convert web link to file download link
def _convert_url(url):
    return url.replace('/view/', '/download/')


def _auth_with_f5site(reqs_obj):
    print "Authenticate with F5..."
    username = raw_input('Enter username: ')
    password = getpass.getpass('Enter password: ')
    # username = ''
    # password = ''
    temp = StringIO.StringIO()
    pickle.dump([username, password], temp)

    requests.post('http://127.0.0.1:63333/auth.do', data=temp.getvalue())

    auth_cookie = reqs_obj.get_cookie(username, password)

    logger.debug("returning value of get_cookie(): %s", auth_cookie)

    # if auth failed, stop sub_daemon and exit the script
    if auth_cookie == int(401):
        toggle.stop_daemon()
        logger.info('authentication failed, shutdown sub_daemon.')
        sys.exit(1)

    temp = StringIO.StringIO()

    try:
        pickle.dump([requests.utils.dict_from_cookiejar(auth_cookie[0]),
                     auth_cookie[1]], temp)
    except Exception as e:
        logger.info(e)
        sys.exit(1)

    # get cookie value: temp.getvalue()
    # update session cookie, expire time to local sub_daemon
    requests.post('http://127.0.0.1:63333', data=temp.getvalue())
    return username, password


def usage():

    print "Qkview Shell(1.1.dev6)"
    print "Upload multiple qkviews to a single case or download " \
          "log file/config file/tmsh command output from ihealth."
    print "    Usage: qksh [[case number] [qkview file]] "
    print "                [url of qkview files] "
    print "                [url of qkview command output]"
    print "    Example:"
    print "        qksh.py <case number> <qkview file list>"
    print "        qksh.py 1-12345678 test-1.qkview test-2.qkview"
    print "        qksh.py <file/command url of iHealth>"
    print "        qksh.py https://ihealth.f5.com/qkview-analyzer/qv/4081581" \
          "/files/download/Y29uZmlnL2JpZ2lwLmNvbmY"
    logger.info('Invalid arguments.')
    sys.exit(1)


def poke_cookie(upload_qkview):

    logger.info('daemon is running, step into poke_cookie().')
    poke_res = requests.get('http://127.0.0.1:63333/poke')

    if poke_res.content == "valid":
        logger.info('session cookie is valid. step out poke_cookie()')
        return
    else:

        # even though pid file exists, cookie appears to be invalid, therefore
        # try to restart the sub_daemon, and re-auth against f5 web site.
        # TODO: need to get sub_daemon stdout to qksh.log file, currently
        # the stdout is suspended.
        logger.info('session cookie is not valid, restarting sub_daemon.')

        try:
            toggle.restart_daemon()
        except Exception as e:
            toggle.forceload_daemon()
            logger.info(e)
            logger.info('force reloading daemon.')

        logger.info('re-auth with F5 iHealth api')
        _auth_with_f5site(upload_qkview)


# check if sub_daemon pid exists or not, if not exists, re-initiate a new
# process.
def pid_check(upload_qkview):

    logger.info('step into pid_check(), checking pid file: %s',
                os.path.isfile('/var/run/credential.pid'))

    ret, pid = toggle.status_daemon()

    logger.debug('print ret value: ', ret)
    if ret == 1 or ret == 3:

        logger.info('daemon is not running, kick off sub_daemon.')

        toggle.start_daemon()

        username, password = _auth_with_f5site(upload_qkview)

        # post username/password in format of list(before pickling),
        # e.g. [username, password]
        cred_cache = StringIO.StringIO()
        pickle.dump([username, password], cred_cache)
        requests.post('http://127.0.0.1:63333/auth.do',
                      data=cred_cache.getvalue())
        logger.info('post done! Step out pid_check()')

    else:
        poke_cookie(upload_qkview)


def main():

    # parsing arguments
    ret = _parse_arg(sys.argv)

    # create class for uploading qkview
    upload_qkview = RetrieveCookie()

    # checking daemon status, validate session cookie etc...
    pid_check(upload_qkview)

    logger.debug('case match? %s', ret)

    if ret == 1:
        # TODO: need to support uploading multiple qkview concurrently.
        upload_qkview.uploadqkview(sys.argv[1], sys.argv[2])

    elif ret == 2:
        upload_qkview.get_file(_convert_url(sys.argv[1]))

    elif ret == 3:
        upload_qkview.get_commands(_convert_url(sys.argv[1]))

    else:
        usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
