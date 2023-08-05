import unittest

import mock

from vmupdate.channel import Channel


class ChannelTestCase(unittest.TestCase):
    TEST_HOST = 'testhost'
    TEST_PORT = 0

    @mock.patch('vmupdate.channel.SSHClient', autospec=True)
    def test_connect(self, mock_ssh):
        test_user = 'testuser'
        test_pass = 'testpass'

        channel = Channel(ChannelTestCase.TEST_HOST, ChannelTestCase.TEST_PORT)

        channel.connect(test_user, test_pass)

        mock_ssh.return_value.connect.assert_called_once_with(ChannelTestCase.TEST_HOST,
                                                              port=ChannelTestCase.TEST_PORT,
                                                              username=test_user,
                                                              password=test_pass)

    @mock.patch('vmupdate.channel.SSHClient', autospec=True)
    def test_close(self, mock_ssh):
        with Channel(ChannelTestCase.TEST_HOST, ChannelTestCase.TEST_PORT):
            pass

        mock_ssh.return_value.close.assert_called_once_with()

    @mock.patch('vmupdate.channel.SSHClient', autospec=True)
    def test_run(self, mock_ssh):
        test_stdin = 'testin'
        test_stdout = 'testout'
        test_stderr = 'testerr'

        mock_ssh.return_value.exec_command.return_value = (test_stdin, test_stdout, test_stderr)

        channel = Channel(ChannelTestCase.TEST_HOST, ChannelTestCase.TEST_PORT)

        cmd = channel.run(['some', 'test', 'command'])

        mock_ssh.return_value.exec_command.assert_called_once_with('some test command')

        self.assertEqual(cmd.stdin, test_stdin)
        self.assertEqual(cmd.stdout, test_stdout)
        self.assertEqual(cmd.stderr, test_stderr)
