import unittest

import mock

from vmupdate.config import config
from vmupdate.shells.posix import Posix
from vmupdate.vm import VM
from vmupdate.virtualizers.virtualizer import Virtualizer

from tests.context import get_data_path


class VMTestCase(unittest.TestCase):
    TEST_UID = 'testmachine'

    @classmethod
    def setUpClass(cls):
        config.load(config_path=get_data_path('testconfig.yaml'))

    def setUp(self):
        self.mock_virt = mock.MagicMock(spec=Virtualizer)
        self.vm = VM(self.mock_virt, VMTestCase.TEST_UID)

    def test_ssh_port(self):
        self.assertEqual(self.vm.ssh_port, config.network.ssh.guest_port)

    def test_start(self):
        self.vm.start()
        self.mock_virt.start_vm.assert_called_once_with(VMTestCase.TEST_UID)

    def test_stop(self):
        self.vm.stop()
        self.mock_virt.stop_vm.assert_called_once_with(VMTestCase.TEST_UID)

    def test_get_status(self):
        test_status = 'teststatus'

        self.mock_virt.get_vm_status.return_value = test_status
        status = self.vm.get_status()

        self.assertEqual(status, test_status)
        self.mock_virt.get_vm_status.assert_called_once_with(VMTestCase.TEST_UID)

    def test_get_os(self):
        test_os = 'testos'

        self.mock_virt.get_vm_os.return_value = test_os
        os = self.vm.get_os()

        self.assertEqual(os, test_os)
        self.mock_virt.get_vm_os.assert_called_once_with(VMTestCase.TEST_UID)

    def test_get_ssh_info(self):
        test_ssh_info = ('testhost', 'testport')

        self.mock_virt.get_ssh_info.return_value = test_ssh_info
        ssh_info = self.vm.get_ssh_info()

        self.assertEqual(ssh_info[0], test_ssh_info[0])
        self.assertEqual(ssh_info[1], test_ssh_info[1])
        self.mock_virt.get_ssh_info.assert_called_once_with(VMTestCase.TEST_UID, self.vm.ssh_port)

    def test_enable_ssh(self):
        test_host_port = 2022
        test_exitcode = -1

        self.mock_virt.enable_ssh.return_value = test_exitcode
        exitcode = self.vm.enable_ssh(test_host_port)

        self.assertEqual(exitcode, test_exitcode)
        self.mock_virt.enable_ssh.assert_called_once_with(VMTestCase.TEST_UID, test_host_port, self.vm.ssh_port)

    @mock.patch('vmupdate.vm.Channel', autospec=True)
    @mock.patch('vmupdate.vm.get_credentials')
    def test_connect(self, mock_get_credentials, mock_channel):
        test_host = 'testhost'
        test_port = 'testport'
        test_user = 'testuser'
        test_pass = 'testpass'

        self.mock_virt.get_ssh_info.return_value = (test_host, test_port)
        mock_get_credentials.return_value = (test_user, test_pass)

        self.mock_virt.get_vm_os.return_value = 'Ubuntu'

        shell = self.vm.connect()

        mock_channel.assert_called_once_with(test_host, test_port)
        mock_channel.return_value.connect.assert_called_once_with(test_user, test_pass)
        self.assertIsInstance(shell, Posix)

    def test_get_shell_name(self):
        self.mock_virt.get_vm_os.return_value = 'Ubuntu'
        self.assertEqual(self.vm.get_shell_name(), 'Posix')
