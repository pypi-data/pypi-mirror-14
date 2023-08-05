import unittest

import mock

from vmupdate.config import config
from vmupdate.host import update_all_vms, get_all_vms, find_virtualizers, get_available_ports
from vmupdate.vm import VM
from vmupdate.virtualizers import VM_STOPPED
from vmupdate.virtualizers.virtualizer import Virtualizer

from tests.context import get_data_path


class HostTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config.load(get_data_path('testconfig.yaml'))

    @mock.patch('time.sleep', autospec=True)
    @mock.patch('vmupdate.host.run_pkgmgr', autospec=True)
    @mock.patch('vmupdate.host.get_pkgmgrs', autospec=True)
    @mock.patch('vmupdate.host.get_available_ports', autospec=True)
    @mock.patch('vmupdate.host.get_all_vms', autospec=True)
    def test_update_all_vms(self, mock_get_all_vms, mock_get_available_ports, mock_get_pkgmgrs, mock_run_pkgmgr, mock_sleep):
        pkgmgr = 'apt-get'
        pkgmgr_cmds = ['update', 'upgrade']
        test_ports = [1, 2, 3]

        mock_vm = mock.MagicMock(spec=VM)
        mock_vm.uid = 'testvm'
        mock_vm.get_status.return_value = VM_STOPPED
        mock_vm.get_ssh_info.return_value = (None, None)

        mock_get_all_vms.return_value = [mock_vm]

        mock_get_available_ports.return_value = test_ports

        mock_get_pkgmgrs.return_value = [(pkgmgr, pkgmgr_cmds)]

        update_all_vms()

        mock_vm.start.assert_called_once_with()
        mock_vm.stop.assert_called_once_with()
        mock_vm.get_ssh_info.assert_called_once_with()
        mock_vm.enable_ssh.assert_called_once_with(test_ports[0])

        mock_sleep.assert_has_calls([mock.call(config.general.wait_after_start),
                                     mock.call(config.general.wait_before_stop)])

        mock_get_pkgmgrs.assert_called_once_with(mock_vm)

        mock_run_pkgmgr.assert_called_once_with(mock_vm, pkgmgr, pkgmgr_cmds)

    @mock.patch('vmupdate.host.get_virtualizer', autospec=True)
    @mock.patch('vmupdate.host.find_virtualizers', autospec=True)
    def test_get_all_vms(self, mock_find_virtualizers, mock_get_virtualizer):
        test_virt_name = 'testvirt'
        test_virt_path = '/test/path'
        test_vm_name = 'testvm'
        test_vm_uuid = 'testuuid'

        mock_find_virtualizers.return_value = {test_virt_name: test_virt_path}

        mock_virt = mock.MagicMock(spec=Virtualizer)

        mock_virt.list_vms.return_value = [(test_vm_name, test_vm_uuid)]

        mock_get_virtualizer.return_value = mock_virt

        vms = get_all_vms()

        mock_get_virtualizer.assert_called_once_with(test_virt_name, test_virt_path)

        self.assertEqual(len(vms), 1)
        self.assertEqual(vms[0].uid, test_vm_name)

    @mock.patch('os.path.isfile', autospec=True)
    @mock.patch('platform.system', autospec=True)
    def test_find_virtualizers(self, mock_system, mock_isfile):
        mock_system.return_value = 'Test OS'
        mock_isfile.return_value = True

        virts = find_virtualizers()

        mock_isfile.assert_called_once_with('/test/path/virt')

        self.assertEqual(virts['TestVirtualizer'], '/test/path/virt')

    def test_get_available_ports(self):
        test_host = 'testhost'
        test_port = 50000

        mock_vm = mock.MagicMock(spec=VM)

        mock_vm.uid = 'testvm'
        mock_vm.get_ssh_info.return_value = (test_host, test_port)

        ports = get_available_ports([mock_vm])

        self.assertEqual(len(ports), 15847)
        self.assertNotIn(test_port, ports)
