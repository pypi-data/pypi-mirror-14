"""
    Provide functions to find and update VM's.
"""

import logging
import os
import platform
import time

from .config import config
from .pkgmgr import get_pkgmgrs, run_pkgmgr
from .virtualizers import get_virtualizer, VM_STOPPED, VM_UNKNOWN
from .vm import VM

log = logging.getLogger(__name__)


def update_all_vms():
    """
        Update all virtual machines on the system.

        :return: exitcode
        :rtype: int
    """

    log.info('Starting update on all VMs')

    vms = _get_all_vms()

    log.info('Found %i VM(s) to update', len(vms))

    available_ports = iter(_get_available_ports(vms))

    for vm in vms:
        vm_orig_status = VM_UNKNOWN

        try:
            if not any(vm.get_ssh_info()):
                if vm.get_status() == VM_STOPPED:
                    log.info('Enabling SSH for %s', vm.uid)
                    vm.enable_ssh(next(available_ports))
                else:
                    log.warn('SSH cannot be enabled for %s unless it is stopped', vm.uid)
                    log.info('Skipping %s', vm.uid)

                    continue

            log.info('Starting update on %s', vm.uid)

            vm_orig_status = vm.get_status()

            if vm_orig_status == VM_STOPPED:
                log.info('Starting %s', vm.uid)
                vm.start()
                time.sleep(config.general.wait_after_start)

            for pkgmgr, cmds in get_pkgmgrs(vm):
                run_pkgmgr(vm, pkgmgr, cmds)
        except:
            log.exception('Failed while updating %s', vm.uid)

        if vm_orig_status == VM_STOPPED:
            log.info('Stopping %s', vm.uid)
            time.sleep(config.general.wait_before_stop)
            vm.stop()

        log.info('Finished update on %s', vm.uid)

    log.info('Finished update on all VMs')

    return 0


def _get_all_vms():
    """
        Return all virtual machines on the system.

        :return: list of virtual machines
        :rtype: list(:class:`~.vm.VM`)
    """

    vms = []

    virtualizers = _find_virtualizers()

    for virt_name, virt_path in virtualizers.items():
        log.info('Querying virtualizer %s', virt_name)

        virtualizer = get_virtualizer(virt_name, virt_path)

        for vm_name, vm_uuid in virtualizer.list_vms():
            log.info('Found VM %s', vm_name)

            vms.append(VM(virtualizer, vm_name))

    return vms


def _find_virtualizers():
    """
        Return all virtualizers found on the system.

        :return: dictionary of names and paths
        :rtype: dict(str, str)
    """

    log.info('Finding virtualizers')

    virtualizers = {}

    for name, paths in config.virtualizers[platform.system()].items():
        try:
            for path in paths:
                path = os.path.expandvars(path)

                log.debug('Checking virtualizer "%s"', path)

                if os.path.isfile(path):
                    virtualizers[name] = path
        except:
            log.exception('Failed while locating virtualizer %s', name)

    return virtualizers


def _get_available_ports(vms):
    """
        Return ports in the configured range not in use by the ``vms``.

        :param vms: list of virtual machines
        :type vms: list(:class:`~.vm.VM`)

        :return: list of ports
        :rtype: list(int)
    """

    used_ports = _get_used_ports(vms)

    min_port = config.network.ssh.host_min_port
    max_port = config.network.ssh.host_max_port

    return [p for p in range(min_port, max_port) if p not in used_ports]


def _get_used_ports(vms):
    """
        Return a set of ports in use by the ``vms``.

        :param vms: list of virtual machines
        :type vms: list(:class:`~.vm.VM`)

        :return: set of ports
        :rtype: set(int)
    """

    used_ports = set()

    for vm in vms:
        ip, port = vm.get_ssh_info()

        if port:
            used_ports.add(port)

    return used_ports
