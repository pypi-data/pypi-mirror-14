import subprocess
import sys
import os
import logging


class ToggleDaemon:

    logger = logging.getLogger('ihealth_api.toggle')

    def __init__(self, pth):
        self.path = pth

    @staticmethod
    def _get_daemon_pid():

        a = os.popen("ps aux | grep -E sub_daemon| grep -v grep").readline()

        if a != '':
            return a.split()[1]
        else:
            return a

    def _kill_daemon(self, ret, pid=0):

        if ret != 0:
            os.system("rm -rf /var/run/credential.pid")
            self.logger.info('clear up PID file.')
        if pid != 0:
            os.system("kill -9 "+str(pid))
            self.logger.info('killing sub_daemon process, PID: %s', pid)

    def status_daemon(self):

        ps_output = self._get_daemon_pid()

        # return value matrix:
        # 0     pid file exists, sub_daemon is running
        # 1     pid file exists, sub_daemon is not running
        # 2     pid file does not exists, sub_daemon is running
        # 3     pid file does not exists, sub_daemon is not running
        # get sub_daemon pid by shell command.
        try:
            with open('/var/run/credential.pid') as f:
                a = f.readline()
            if ps_output == '':
                self.logger.info('PID file exists, sub_daemon is not running.')

                # second int is pid, default is 0, meaning sub_daemon is
                # not running.
                return 1, 0
        except Exception as e:
            self.logger.info(e)
            self.logger.info('PID file open failed.')
            if ps_output != '':
                self.logger.info(
                    'Sub_daemon is running, PID file is not exists. PID: %s',
                    ps_output)
                return 2, ps_output
            self.logger.info('Sub_daemon is not running.')
            return 3, 0

        if a.strip('\n') == ps_output:
            self.logger.info('Daemon is running, PID file exists. PID: %s',
                             a.strip('\n'))
            return 0, a.strip('\n')

    def start_daemon(self):
        self.logger.info('calling subprocess, start off sub_daemon')
        self.logger.info(self.path)
        subprocess.check_call(
            [sys.executable, self.path, 'start'])
        self.logger.info('sub_daemon started')

    def stop_daemon(self):
        ret, pid = self.status_daemon()
        self.logger.debug(
            'PID returned by status_daemon: %s, ret value %s', pid, ret)

        if ret != 0:
            self._kill_daemon(ret, pid)
        else:
            subprocess.check_call(
                [sys.executable, self.path, 'stop'])

    def restart_daemon(self):
        try:
            subprocess.check_call(
                [sys.executable, self.path, 'stop'])
        except Exception as e:
            self.logger.info(e)
        subprocess.check_call(
            [sys.executable, self.path, 'start'])

    def reload_daemon(self):
        self.restart_daemon()

    def forceload_daemon(self):

        ret, pid = self.status_daemon()
        self.logger.debug(
            'PID returned by status_daemon: %s, ret value %s', pid, ret)
        if ret != 0:
            self._kill_daemon(ret, pid)
        subprocess.check_call(
            [sys.executable, self.path, 'start'])
