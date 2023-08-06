import unittest

from vmupdate.shells import get_shell, Shell, Posix
from vmupdate.channel import Channel

from tests.constants import *
from tests.context import mock
from tests.mocks import get_mock_ssh_client


class ShellTestCase(unittest.TestCase):
    def setUp(self):
        patch_shell = mock.patch.multiple(Shell, __abstractmethods__=set())

        patch_shell.start()

        self.addCleanup(patch_shell.stop)

        self.shell = Shell()
        self.shell.channel = mock.MagicMock(spec=Channel)

    def test_enter(self):
        shell = self.shell.__enter__()

        self.assertIs(shell, self.shell)

    def test_exit(self):
        self.shell.__exit__(None, None, None)

        self.shell.channel.close.assert_called_once_with()

    def test_run(self):
        test_args = ['test', 'args']

        self.shell.run(test_args)

        self.shell.channel.run.assert_called_once_with(test_args)

    def test_close(self):
        self.shell.close()

        self.shell.channel.close.assert_called_once_with()


class PosixTestCase(unittest.TestCase):
    def setUp(self):
        patch_ssh = mock.patch('vmupdate.channel.SSHClient', new_callable=get_mock_ssh_client)

        self.addCleanup(patch_ssh.stop)

        self.mock_ssh = patch_ssh.start()

        self.channel = Channel(TEST_HOST, TEST_HOST_PORT)
        self.shell = Posix(self.channel)

    def test_get_shell(self):
        shell = get_shell('Posix', None)

        self.assertIs(type(shell), Posix)

    def test_command_exists(self):
        test_command = 'testcommand'

        success = self.shell.command_exists(test_command)

        self.mock_ssh.return_value.exec_command.assert_called_once_with('command -v {0}'.format(test_command))
        self.assertTrue(success)

    def test_run_as_elevated(self):
        test_command = 'testcommand'

        cmd = self.shell.run_as_elevated(test_command, TEST_PASS)

        self.mock_ssh.return_value.exec_command.assert_called_once_with('sudo -S {0}'.format(test_command))

        cmd.stdin.write.assert_has_calls([mock.call(TEST_PASS), mock.call('\n')])
        cmd.stdin.flush.assert_called_once_with()
