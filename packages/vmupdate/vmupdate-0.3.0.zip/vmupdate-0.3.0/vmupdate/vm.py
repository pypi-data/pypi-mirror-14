"""
    Provide a wrapper class around VM interactions.
"""

from .channel import Channel
from .config import config
from .credentials import get_credentials
from .errors import SshError
from .shells import get_shell


class VM(object):
    """
        Provide virtual machine interface.

        :ivar virtualizer: virtualizer that the virtual machine runs under
        :ivar str uid: identifier of the virtual machine
        :vartype virtualizer: :class:`~.virtualizers.Virtualizer`
    """

    def __init__(self, virtualizer, uid):
        """
            Return an instance of :class:`VM`.

            :param virtualizer: virtualizer that the virtual machine runs under
            :param str uid: identifier of the virtual machine
            :type virtualizer: :class:`~.virtualizers.Virtualizer`

            :rtype:`VM`
        """

        self.virtualizer = virtualizer
        self.uid = uid

    @property
    def ssh_port(self):
        """
            Return the SSH port of the guest.

            :rtype: int
        """

        return config.network.ssh.guest_port

    @property
    def shell_name(self):
        """
            Return the name of the shell.

            :rtype: str
        """

        if self.uid in config.machines and config.machines[self.uid].shell:
            return config.machines[self.uid].shell

        return config.shells.get(self.virtualizer.get_vm_os(self.uid))

    def start(self):
        """
            Start the virtual machine.

            :return: exitcode
            :rtype: int
        """

        return self.virtualizer.start_vm(self.uid)

    def stop(self):
        """
            Stop the virtual machine.

            :return: exitcode
            :rtype: int
        """

        return self.virtualizer.stop_vm(self.uid)

    def get_status(self):
        """
            Return the status of the virtual machine.

            Possible values can be found in :mod:`.constants`.

            :rtype: str
        """

        return self.virtualizer.get_vm_status(self.uid)

    def get_os(self):
        """
            Return the operating system of the virtual machine.

            Possible values can be found in :mod:`.constants`.

            :rtype: str
        """

        return self.virtualizer.get_vm_os(self.uid)

    def get_ssh_info(self):
        """
            Return the SSH connection information for the virtual machine.

            :return: tuple of (hostname, port)
            :rtype: (str, int)
        """

        return self.virtualizer.get_ssh_info(self.uid, self.ssh_port)

    def enable_ssh(self, host_port):
        """
            Enable SSH port forwarding for the virtual machine.

            :param int host_port: the post on the host to forward to the guest

            :return: exitcode
            :rtype: int
        """

        return self.virtualizer.enable_ssh(self.uid, host_port, self.ssh_port)

    def connect(self):
        """
            Connect to the virtual machine and return a shell.

            :rtype: :class:`~.shells.Shell`
        """

        ip, port = self.get_ssh_info()

        if not ip and not port:
            raise SshError('SSH is not enabled for %s' % self.uid)

        channel = Channel(ip, port)

        username, password = get_credentials(self.uid)

        channel.connect(username, password)

        return get_shell(self.shell_name, channel)
