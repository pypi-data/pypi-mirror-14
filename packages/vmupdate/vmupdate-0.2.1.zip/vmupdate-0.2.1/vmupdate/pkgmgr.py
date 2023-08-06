"""
    Provide functions to query and command package managers.
"""

import logging

from .config import config
from .credentials import get_credentials, get_run_as_elevated
from .errors import UpdateError

log = logging.getLogger(__name__)


def get_pkgmgrs(vm):
    """
        Return all package managers on the virtual machine.

        :param vm: virtual machine to target
        :type vm: :class:`~.vm.VM`

        :return: list of tuples of (name, list of paths)
        :rtype: list((str, list(str)))
    """

    pkgmgrs = []
    vm_os = vm.get_os()

    log.info('Querying package managers for %s on OS %s', vm.uid, vm_os)

    if vm_os in config.pkgmgrs:
        with vm.connect() as shell:
            for pkgmgr, cmds in config.pkgmgrs[vm_os].items():
                log.debug('Checking if %s exists on %s', pkgmgr, vm.uid)

                if shell.command_exists(pkgmgr):
                    pkgmgrs.append((pkgmgr, cmds))

    return pkgmgrs


def run_pkgmgr(vm, pkgmgr, cmds):
    """
        Run the package manager commands on the virtual machine in sequence.

        :param vm: virtual machine to target
        :param str pkgmgr: name of the package manager to run
        :param cmds: list of commands to run in sequence
        :type vm: :class:`~.vm.VM`
        :type cmds: list(str)

        :raise UpdateError: if any command does not exit with ``0``
    """

    log.info('Updating %s on %s', pkgmgr, vm.uid)

    with vm.connect() as shell:
        for cmd in cmds:
            cmd = _run_pkgmgr_cmd(vm, shell, pkgmgr, cmd)

            if cmd.wait() != 0:
                raise UpdateError('Update failed')


def _run_pkgmgr_cmd(vm, shell, pkgmgr, cmd):
    """
        Run the package manager command on the virtual machine.

        :param vm: virtual machine to target
        :param shell: the shell to run the command against
        :param str pkgmgr: name of the package manager to run
        :param str cmd: command to run
        :type vm: :class:`~.vm.VM`
        :type shell: :class:`~.shells.Shell`

        :return: channel command
        :rtype: :class:`~.channel.ChannelCommand`
    """

    shell_cmd = ' '.join([pkgmgr, cmd])

    log.debug('Running %s on %s', shell_cmd, vm.uid)

    if get_run_as_elevated(vm.uid):
        username, password = get_credentials(vm.uid)

        return shell.run_as_elevated(shell_cmd, password)

    return shell.run(shell_cmd)
