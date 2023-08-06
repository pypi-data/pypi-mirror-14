"""
    Provide a transparent abstraction for interacting with virtualizers.
"""

from abc import ABCMeta, abstractmethod
import logging
import re
import subprocess
import sys

from vmupdate.constants import *

log = logging.getLogger(__name__)


def get_virtualizer(name, path):
    """
        Return an instance of a virtualizer.

        The virtualizer should extend :class:`Virtualizer`.

        :param str name: name of the virtualizer class to instantiate
        :param str path: path of the virtualizer to pass to the constructor
    """

    virtualizer_class = getattr(sys.modules[__name__], name)

    return virtualizer_class(path)


class Virtualizer(object):
    """
        Abstract virtualizer control.

        This class must be inherited and cannot be used directly.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def list_vms(self):
        """
            Return all virtual machines.

            This is a virtualizer-specific command and must be overridden.

            :return: list of tuple (name, id)
            :rtype: list(str, str)
        """

        pass

    @abstractmethod
    def start_vm(self, uid):
        """
            Start the virtual machine.

            This is a virtualizer-specific command and must be overridden.

            :param str uid: identifier of the machine

            :return: exitcode
            :rtype: int
        """

        pass

    @abstractmethod
    def stop_vm(self, uid):
        """
            Stop the virtual machine.

            This is a virtualizer-specific command and must be overridden.

            :param str uid: identifier of the machine

            :return: exitcode
            :rtype: int
        """

        pass

    @abstractmethod
    def get_vm_status(self, uid):
        """
            Return the status of the virtual machine.

            This is a virtualizer-specific command and must be overridden.

            Possible values can be found in :mod:`.constants`.

            :param str uid: identifier of the machine

            :rtype: str
        """

        pass

    @abstractmethod
    def get_vm_os(self, uid):
        """
            Return the operating system of the virtual machine.

            This is a virtualizer-specific command and must be overridden.

            Possible values can be found in :mod:`.constants`.

            :param str uid: identifier of the machine

            :rtype: str
        """

        pass

    @abstractmethod
    def get_ssh_info(self, uid, ssh_port):
        """
            Return the SSH connection information for the virtual machine.

            This is a virtualizer-specific command and must be overridden.

            :param str uid: identifier of the machine
            :param int ssh_port: expected SSH port of the guest

            :return: tuple of (hostname, port)
            :rtype: (str, int)
        """

        pass

    @abstractmethod
    def enable_ssh(self, uid, host_port, guest_port):
        """
            Enable SSH port forwarding for the virtual machine.

            This is a virtualizer-specific command and must be overridden.

            :param str uid: identifier of the machine
            :param int host_port: the post on the host to forward to the guest
            :param int guest_port: SSH port of the guest

            :return: exitcode
            :rtype: int
        """

        pass


class VirtualBox(Virtualizer):
    """Control the VirtualBox virtualizer."""

    def __init__(self, manager_path):
        """
            Return an instance of :class:`VirtualBox`.

            :param str manager_path: path to the VirtualBox control utility

            :rtype:`VirtualBox`
        """

        self._manager_path = manager_path

    def list_vms(self):
        """
            Return all virtual machines.

            :return: list of tuple (name, id)
            :rtype: list(str, str)
        """

        cmd = subprocess.Popen([self._manager_path, 'list', 'vms'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        vms = []

        stdoutdata, stderrdata = cmd.communicate()

        if stderrdata:
            log.error(stderrdata)

        if stdoutdata:
            matches = re.finditer(r"""^"(?P<name>[^"]+)"\s+\{(?P<uuid>[^}]+)\}""",
                                  stdoutdata,
                                  flags=re.IGNORECASE | re.MULTILINE)

            if matches:
                for match in matches:
                    vms.append((match.group('name'), match.group('uuid')))

        return vms

    def start_vm(self, uid):
        """
            Start the virtual machine.

            :param str uid: identifier of the machine

            :return: exitcode
            :rtype: int
        """

        cmd = subprocess.Popen([self._manager_path, 'startvm', uid, '--type', 'headless'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        stdoutdata, stderrdata = cmd.communicate()

        if stderrdata:
            log.error(stderrdata)

        return cmd.wait()

    def stop_vm(self, uid):
        """
            Stop the virtual machine.

            :param str uid: identifier of the machine

            :return: exitcode
            :rtype: int
        """

        cmd = subprocess.Popen([self._manager_path, 'controlvm', uid, 'poweroff'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        return cmd.wait()

    def get_vm_status(self, uid):
        """
            Return the status of the virtual machine.

            Possible values can be found in :mod:`.constants`.

            :param str uid: identifier of the machine

            :rtype: str
        """

        cmd = subprocess.Popen([self._manager_path, 'showvminfo', uid],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        stdoutdata, stderrdata = cmd.communicate()

        if stderrdata:
            log.error(stderrdata)

        if stdoutdata:
            match = re.search(r"""^State:\s*(?P<state>[a-z\s]*)""",
                              stdoutdata, flags=re.IGNORECASE | re.MULTILINE)

            if match:
                state = match.group('state').strip().lower()

                if state == 'powered off' or state == 'aborted':
                    return VM_STOPPED
                elif state == 'running':
                    return VM_RUNNING
                elif state == 'saved':
                    return VM_SUSPENDED
                elif state == 'paused':
                    return VM_PAUSED

        return VM_UNKNOWN

    def get_vm_os(self, uid):
        """
            Return the operating system of the virtual machine.

            Possible values can be found in :mod:`.constants`.

            :param str uid: identifier of the machine

            :rtype: str
        """
        cmd = subprocess.Popen([self._manager_path, 'showvminfo', uid],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        stdoutdata, stderrdata = cmd.communicate()

        if stderrdata:
            log.error(stderrdata)

        if stdoutdata:
            match = re.search(r"""^Guest OS:\s*(?P<os>[a-z\s]*)""", stdoutdata, flags=re.IGNORECASE | re.MULTILINE)

            if match:
                state = match.group('os').strip().lower()

                if state in ('windows', 'windows xp', 'windows vista', 'other windows'):
                    return OS_WINDOWS
                elif state == 'mac os x':
                    return OS_MAC_OS_X
                elif state == 'linux':
                    return OS_LINUX
                elif state == 'arch linux':
                    return OS_ARCH
                elif state == 'ubuntu':
                    return OS_UBUNTU
                elif state == 'red hat':
                    return OS_REDHAT
                elif state == 'debian':
                    return OS_DEBIAN
                elif state == 'fedora':
                    return OS_FEDORA
                elif state == 'gentoo':
                    return OS_GENTOO
                elif state == 'opensuse':
                    return OS_OPENSUSE
                elif state == 'mandriva':
                    return OS_MANDRIVA
                elif state == 'turbolinux':
                    return OS_TURBOLINUX
                elif state == 'xandros':
                    return OS_XANDROS
                elif state == 'oracle':
                    return OS_ORACLE

        return OS_UNKNOWN

    def get_ssh_info(self, uid, ssh_port):
        """
            Return the SSH connection information for the virtual machine.

            :param str uid: identifier of the machine
            :param int ssh_port: expected SSH port of the guest

            :return: tuple of (hostname, port)
            :rtype: (str, int)
        """

        cmd = subprocess.Popen([self._manager_path, 'showvminfo', uid], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)

        stdoutdata, stderrdata = cmd.communicate()

        if stderrdata:
            log.error(stderrdata)

        if stdoutdata:
            matches = re.finditer(r"""^NIC \d+ Rule\(\d+\):\s*name = (?P<name>[^,]*), """
                                  """protocol = (?P<protocol>(tcp|udp)), """
                                  """host ip = (?P<hostname>(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3})?), """
                                  """host port = (?P<hostport>\d*), """
                                  """guest ip = (?P<guestip>(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3})?), """
                                  """guest port = (?P<guestport>\d*)""",
                                  stdoutdata, flags=re.IGNORECASE | re.MULTILINE)

            if matches:
                for match in matches:
                    if match.group('protocol').lower() == 'tcp' and int(match.group('guestport')) == ssh_port:
                        return match.group('hostname') or '127.0.0.1', int(match.group('hostport'))

        return None, None

    def enable_ssh(self, uid, host_port, guest_port):
        """
            Enable SSH port forwarding for the virtual machine.

            :param str uid: identifier of the machine
            :param int host_port: the post on the host to forward to the guest
            :param int guest_port: SSH port of the guest

            :return: exitcode
            :rtype: int
        """

        cmd = subprocess.Popen([self._manager_path, 'modifyvm', uid,
                                '--natpf1', 'ssh,tcp,,{0},,{1}'.format(host_port, guest_port)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        stdoutdata, stderrdata = cmd.communicate()

        if stderrdata:
            log.error(stderrdata)

        return cmd.wait()
