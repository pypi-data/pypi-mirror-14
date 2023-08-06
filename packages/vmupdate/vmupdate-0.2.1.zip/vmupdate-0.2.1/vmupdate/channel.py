"""
    Provide wrapper classes around virtual machine communication.
"""

import logging
from subprocess import list2cmdline

from paramiko import SSHClient, AutoAddPolicy

log = logging.getLogger(__name__)


class Channel(object):
    """
        Provide virtual machine communication.

        :ivar str hostname: name or IP of the virtual machine
        :ivar int port: port of the virtual machine
    """

    def __init__(self, hostname, port):
        """
            Return an instance of :class:`Channel`.

            :param str hostname: name or IP of the virtual machine to connect to
            :param int port: port of the virtual machine to connect to

            :rtype:`Channel`
        """

        self.hostname = hostname
        self.port = port

        self._ssh = SSHClient()

    def __enter__(self):
        """
            Return instance of :class:`Channel`.

            :rtype:`Channel`
        """

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection and release resources."""

        self.close()

    def connect(self, username, password):
        """
            Connect to the virtual machine.

            :param str username: username for authentication
            :param str password: password for authentication
        """

        self._ssh.set_missing_host_key_policy(AutoAddPolicy())
        self._ssh.connect(self.hostname, port=self.port, username=username, password=password)

    def run(self, args):
        """
            Run command against the virtual machine and return a :class:`ChannelCommand`.

            .. warnings also:: :meth:`connect` must be called first.

            :param args: the command to be run
            :type args: str or list

            :rtype: :class:`ChannelCommand`
        """

        if isinstance(args, list):
            args = list2cmdline(args)

        log.debug('Running command: %s', args)

        stdin, stdout, stderr = self._ssh.exec_command(args)

        return ChannelCommand(stdin, stdout, stderr)

    def close(self):
        """Close connection and release resources."""

        if self._ssh:
            self._ssh.close()


class ChannelCommand(object):
    """
        Contain pipes returned from executed command.

        :ivar pipe stdin: standard input
        :ivar pipe stdout: standard output
        :ivar pipe stderr: standard error
    """

    def __init__(self, stdin, stdout, stderr):
        """
            Return an instance of :class:`ChannelCommand`.

            :param pipe stdin: standard input
            :param pipe stdout: standard output
            :param pipe stderr: standard error

            :rtype: :class:`ChannelCommand`
        """

        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def wait(self):
        """
            Wait for the command to complete and return the exit code.

            :rtype: int
        """

        for line in self.stdout:
            log.debug(line.rstrip())

        for line in self.stderr:
            if not line.startswith('[sudo]'):
                log.error(line.rstrip())

        return self.stdout.channel.recv_exit_status()
