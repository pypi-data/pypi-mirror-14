import unittest

import mock

from vmupdate.channel import ChannelCommand
from vmupdate.config import config
from vmupdate.pkgmgr import get_pkgmgrs, run_pkgmgr, run_pkgmgr_cmd
from vmupdate.shells.posix import Posix
from vmupdate.vm import VM

from tests.context import get_data_path


class PkgMgrTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config.load(get_data_path('testconfig.yaml'))

    def setUp(self):
        self.mock_vm = mock.MagicMock(spec=VM)

        self.mock_vm.uid = 'Test Machine 1'
        self.mock_vm.get_os.return_value = 'Ubuntu'

        self.mock_shell = mock.MagicMock(spec=Posix)
        self.mock_shell.command_exists.return_value = True

        self.mock_vm.connect.return_value = self.mock_shell

    def test_get_pkgmgrs(self):
        pkgmgrs = get_pkgmgrs(self.mock_vm)

        self.assertEqual(len(pkgmgrs), 1)
        self.assertEqual(pkgmgrs[0][0], 'apt-get')

    @mock.patch('vmupdate.pkgmgr.run_pkgmgr_cmd', autospec=True)
    def test_run_pkgmgr(self, mock_run_pkgmgr_cmd):
        mock_cmd = mock.MagicMock(spec=ChannelCommand)
        mock_cmd.wait.return_value = 0

        mock_run_pkgmgr_cmd.return_value = mock_cmd

        run_pkgmgr(self.mock_vm, 'apt-get', ['update', 'upgrade'])

        mock_run_pkgmgr_cmd.assert_any_call(mock.ANY, mock.ANY, 'apt-get', 'update')
        mock_run_pkgmgr_cmd.assert_any_call(mock.ANY, mock.ANY, 'apt-get', 'upgrade')

    def test_run_pkgmgr_cmd(self):
        self.mock_vm.uid = 'Test Machine 2'

        run_pkgmgr_cmd(self.mock_vm, self.mock_shell, 'apt-get', 'update')

        self.mock_shell.run.assert_called_once_with('apt-get update')

    def test_run_pkgmgr_cmd_as_elevated(self):
        self.mock_vm.uid = 'Test Machine 1'

        run_pkgmgr_cmd(self.mock_vm, self.mock_shell, 'apt-get', 'update')

        self.mock_shell.run_as_elevated.assert_called_once_with('apt-get update', 'testpass1')
