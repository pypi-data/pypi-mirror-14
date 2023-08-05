#!/bin/bash/env python
from ihealth_api import RetrieveCookie
from distutils.sysconfig import get_python_lib
import sys
import re
import os
import requests
import subprocess
import StringIO
import pickle
import getpass
import logging


# TODO: need to move to logging system
logger = logging.getLogger('qksh')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt='%(asctime)s %(levelname)s %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
fh = logging.FileHandler("/var/log/qksh.log")
fh.setFormatter(formatter)
logger.addHandler(fh)


def usage():
    print "Usage: qksh [[case number] [qkview file]] [url of qkview files]" \
          " [url of qkview command output]\n"
    print "Upload multiple qkview to a single case or download " \
          "log file/bigip.conf file/tmsh command output from ihealth.\n"
    print "Example:\n"
    print "qksh.py <case number> <qkview file list>"
    print "qksh.py 1-12345678 test-1.qkview test-2.qkview"
    print "qksh.py <file/command url of iHealth>"
    print "qksh.py https://ihealth.f5.com/qkview-analyzer/qv/4081581/" \
          "files/download/Y29uZmlnL2JpZ2lwLmNvbmY"


def _get_qksh_site_package_path():
    return get_python_lib()+'/qksh/sub_daemon.py'
    # return 'sub_daemon.py'


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

    temp = StringIO.StringIO()
    pickle.dump([requests.utils.dict_from_cookiejar(auth_cookie[0]),
                 auth_cookie[1]], temp)

    # get cookie value: temp.getvalue()
    # update session cookie, expire time to local sub_daemon
    requests.post('http://127.0.0.1:63333', data=temp.getvalue())
    return username, password


def poke_cookie(upload_qkview):

    logger.info('pid file exists, step into poke_cookie().')
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
        subprocess.check_call(
            [sys.executable, _get_qksh_site_package_path(), 'stop'])
        subprocess.check_call(
            [sys.executable, _get_qksh_site_package_path(), 'start'])

        logger.info('re-auth with F5 iHealth api')
        _auth_with_f5site(upload_qkview)


# check if sub_daemon pid exists or not, if not exists, re-initiate a new
# process.
def pid_check(upload_qkview):

    logger.info('step into pid_check(), checking pid file: %s',
                os.path.isfile('/var/run/credential.pid'))

    if os.path.isfile('/var/run/credential.pid') is False:

        logger.info('pid file not exists, kick off sub_daemon.')
        subprocess.check_call(
            [sys.executable, _get_qksh_site_package_path(), 'start'])

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
    # compile regex pattern for later use
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
                str(sys.argv[1:]).strip('[]'))

    if len(sys.argv) > 1:
        logger.info('parsing arguments.')
        argv_list = sys.argv[1].split('/')
        case_num_match = ptn_case.match(sys.argv[1])
        url_match = ptn_url.match(sys.argv[1])
    else:
        usage()
        sys.exit(1)

    upload_qkview = RetrieveCookie()

    pid_check(upload_qkview)

    logger.debug('case match? %s', case_num_match)
    if case_num_match is not None:

        # need to support uploading multiple qkview concurrently.
        logger.info('uploading qkview.')
        upload_qkview.uploadqkview(sys.argv[1], sys.argv[2])
        logger.info('qkview uploaded.')

    elif url_match is not None:
        if argv_list[6] == 'files':

            logger.info('downloading file.')
            upload_qkview.get_file(sys.argv[1])
            logger.info('file downloaded.')

        if argv_list[6] == 'commands':

            logger.info('downloading command output.')
            upload_qkview.get_commands(sys.argv[1])
            logger.info('commnand output downloaded.')
    else:
        usage()
        sys.exit(1)


if __name__ == "__main__":

    main()
