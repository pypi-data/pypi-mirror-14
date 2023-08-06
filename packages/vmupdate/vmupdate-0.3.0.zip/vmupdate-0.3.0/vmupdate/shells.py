"""
    Provide a transparent abstraction for interacting with shells.
"""

from abc import ABCMeta, abstractmethod
import shlex
import sys

from future.utils import with_metaclass


def get_shell(name, channel):
    """
        Return an instance of a shell.

        The shell should extend :class:`~.Shell`.

        :param str name: name of the shell class to instantiate
        :param channel: channel instance to pass to the constructor
        :type channel: :class:`~.channel.Channel`
    """

    shell_class = getattr(sys.modules[__name__], name)

    return shell_class(channel)


class Shell(with_metaclass(ABCMeta)):
    """
        Abstract virtual machine shell that communicates through a channel.

        This class must be inherited and cannot be used directly.

        :ivar channel: channel used for virtual machine communication
        :vartype channel: :class:`~.channel.Channel`
    """

    def __enter__(self):
        """
            Return instance of :class:`Shell`.

            :rtype:`Shell`
        """

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Close channel and release resources."""

        self.close()

    def run(self, args):
        """
            Run command against the virtual machine.

            :param args: the command to be run
            :type args: str or list

            :rtype: :class:`~.channel.ChannelCommand`
        """

        return self.channel.run(args)

    def close(self):
        """Close channel and release resources."""

        if self.channel:
            self.channel.close()

    @abstractmethod
    def command_exists(self, command):
        """
            Return whether the ``command`` exists in the shell.

            This is a shell-specific command and must be overridden.

            :param str command: name of the command

            :rtype: bool
        """

        pass

    @abstractmethod
    def run_as_elevated(self, args, password):
        """
            Run command against the virtual machine as an elevated user.

            This is a shell-specific command and must be overridden.

            :param args: the command to be run
            :param str password: password to be used for elevated authentication
            :type args: str or list

            :rtype: :class:`~.channel.ChannelCommand`
        """

        pass


class Posix(Shell):
    """
        Represent a POSIX shell that communicates through a channel.

        :ivar channel: channel used for virtual machine communication
        :vartype channel: :class:`~.channel.Channel`
    """

    def __init__(self, channel):
        """
            Return an instance of :class:`Posix`.

            :param channel: channel used for virtual machine communication
            :type channel: :class:`~.channel.Channel`

            :rtype:`Posix`
        """

        self.channel = channel

    def command_exists(self, command):
        """
            Return whether the ``command`` exists in the shell.

            :param str command: name of the command

            :rtype: bool
        """

        cmd = self.run(['command', '-v', command])

        return cmd.wait() == 0

    def run_as_elevated(self, args, password):
        """
            Run command against the virtual machine as an elevated user.

            :param args: the command to be run
            :param str password: password to be used for elevated authentication
            :type args: str or list

            :rtype: :class:`~.channel.ChannelCommand`
        """

        if isinstance(args, str):
            args = shlex.split(args)

        elevated_args = ['sudo', '-S']
        elevated_args.extend(args)

        cmd = self.run(elevated_args)

        cmd.stdin.write(password)
        cmd.stdin.write('\n')
        cmd.stdin.flush()

        return cmd
