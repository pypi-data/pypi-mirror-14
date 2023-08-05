import logging
from subprocess import list2cmdline

from paramiko import SSHClient, AutoAddPolicy

log = logging.getLogger(__name__)


class Channel(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.ssh = SSHClient()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self, username, password):
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(self.ip, port=self.port, username=username, password=password)

    def run(self, args):
        if isinstance(args, list):
            args = list2cmdline(args)

        log.debug('Running command: %s', args)

        stdin, stdout, stderr = self.ssh.exec_command(args)

        return ChannelCommand(stdin, stdout, stderr)

    def close(self):
        if self.ssh:
            self.ssh.close()


class ChannelCommand(object):
    def __init__(self, stdin, stdout, stderr):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def wait(self):
        for line in self.stdout:
            log.debug(line)

        for line in self.stderr:
            log.error(line)

        return self.stdout.channel.recv_exit_status()
