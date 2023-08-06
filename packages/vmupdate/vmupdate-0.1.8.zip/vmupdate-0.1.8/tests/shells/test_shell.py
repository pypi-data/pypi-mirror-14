import unittest

import mock

from vmupdate.shells.shell import Shell
from vmupdate.channel import Channel


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
