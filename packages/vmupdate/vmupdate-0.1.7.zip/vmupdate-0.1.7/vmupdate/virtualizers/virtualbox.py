import logging
import re
import subprocess

from .constants import *
from .virtualizer import Virtualizer

log = logging.getLogger(__name__)


class VirtualBox(Virtualizer):
    def __init__(self, manager_path):
        self.manager_path = manager_path

    def list_vms(self):
        cmd = subprocess.Popen([self.manager_path, 'list', 'vms'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
        cmd = subprocess.Popen([self.manager_path, 'startvm', uid, '--type', 'headless'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdoutdata, stderrdata = cmd.communicate()

        if stderrdata:
            log.error(stderrdata)

        return cmd.wait()

    def stop_vm(self, uid):
        cmd = subprocess.Popen([self.manager_path, 'controlvm', uid, 'poweroff'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return cmd.wait()

    def get_vm_status(self, uid):
        cmd = subprocess.Popen([self.manager_path, 'showvminfo', uid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdoutdata, stderrdata = cmd.communicate()

        if stderrdata:
            log.error(stderrdata)

        if stdoutdata:
            match = re.search(r"""^State:\s*(?P<state>[a-z\s]*)""", stdoutdata, flags=re.IGNORECASE | re.MULTILINE)

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
        cmd = subprocess.Popen([self.manager_path, 'showvminfo', uid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdoutdata, stderrdata = cmd.communicate()

        if stderrdata:
            log.error(stderrdata)

        if stdoutdata:
            match = re.search(r"""^Guest OS:\s*(?P<os>[a-z\s]*)""", stdoutdata, flags=re.IGNORECASE | re.MULTILINE)

            if match:
                state = match.group('os').strip().lower()

                if state == 'windows' or state == 'windows xp' or state == 'windows vista' or state == 'other windows':
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
        cmd = subprocess.Popen([self.manager_path, 'showvminfo', uid], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdoutdata, stderrdata = cmd.communicate()

        if stderrdata:
            log.error(stderrdata)

        if stdoutdata:
            matches = re.finditer(r"""^NIC \d+ Rule\(\d+\):\s*name = (?P<name>[^,]*), protocol = (?P<protocol>(tcp|udp)), host ip = (?P<hostip>(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3})?), host port = (?P<hostport>\d*), guest ip = (?P<guestip>(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3})?), guest port = (?P<guestport>\d*)""", stdoutdata, flags=re.IGNORECASE | re.MULTILINE)

            if matches:
                for match in matches:
                    if match.group('protocol').lower() == 'tcp' and int(match.group('guestport')) == ssh_port:
                        return match.group('hostip') or '127.0.0.1', int(match.group('hostport'))

        return None, None

    def enable_ssh(self, uid, host_port, guest_port):
        cmd = subprocess.Popen([self.manager_path, 'modifyvm', uid, '--natpf1', 'ssh,tcp,,{0},,{1}'.format(host_port, guest_port)])

        stdoutdata, stderrdata = cmd.communicate()

        if stderrdata:
            log.error(stderrdata)

        return cmd.wait()
