import mock

from vmupdate.config import config
from vmupdate.errors import SshError
from vmupdate.shells import Posix
from vmupdate.vm import VM

from tests.case import TestCase
from tests.constants import *
from tests.context import get_data_path
from tests.mocks import get_mock_virtualizer


class VMTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        config.load(config_path=get_data_path('testconfig.yaml'))

    def setUp(self):
        self.mock_virt = get_mock_virtualizer()
        self.vm = VM(self.mock_virt, TEST_UID)

    def test_ssh_port(self):
        self.assertEqual(self.vm.ssh_port, config.network.ssh.guest_port)

    def test_start(self):
        self.vm.start()

        self.mock_virt.start_vm.assert_called_once_with(TEST_UID)

    def test_stop(self):
        self.vm.stop()

        self.mock_virt.stop_vm.assert_called_once_with(TEST_UID)

    def test_get_status(self):
        status = self.vm.get_status()

        self.assertEqual(status, TEST_STATUS)

    def test_get_os(self):
        os = self.vm.get_os()

        self.assertEqual(os, TEST_OS)

    def test_get_ssh_info(self):
        host, port = self.vm.get_ssh_info()

        self.assertEqual(host, TEST_HOST)
        self.assertEqual(port, TEST_HOST_PORT)

        self.mock_virt.get_ssh_info.assert_called_once_with(TEST_UID, self.vm.ssh_port)

    def test_enable_ssh(self):
        exitcode = self.vm.enable_ssh(TEST_HOST_PORT)

        self.assertEqual(exitcode, TEST_EXITCODE)
        self.mock_virt.enable_ssh.assert_called_once_with(TEST_UID, TEST_HOST_PORT, self.vm.ssh_port)

    @mock.patch('vmupdate.vm.Channel', autospec=True)
    def test_connect(self, mock_channel):
        shell = self.vm.connect()

        mock_channel.assert_called_once_with(TEST_HOST, TEST_HOST_PORT)
        mock_channel.return_value.connect.assert_called_once_with(TEST_USER, TEST_PASS)
        self.assertIsInstance(shell, Posix)

    def test_connect_ssh_error(self):
        self.mock_virt.get_ssh_info.return_value = (None, None)

        self.assertRaises(SshError, self.vm.connect)

    def test_get_shell_name(self):
        os = self.mock_virt.get_vm_os()

        self.assertEqual(self.vm.shell_name, config.shells[os])

    def test_get_shell_name_by_machine(self):
        self.vm.uid = 'Test Machine 2'

        self.assertEqual(self.vm.shell_name, 'TestShell')
