from vmupdate.channel import Channel

from tests.case import TestCase
from tests.constants import *
from tests.mocks import get_mock_ssh_client


class ChannelTestCase(TestCase):
    def setUp(self):
        self.mock_ssh = self.add_mock('vmupdate.channel.SSHClient', new_callable=get_mock_ssh_client)

        self.channel = Channel(TEST_HOST, TEST_HOST_PORT)

    def test_connect(self):
        self.channel.connect(TEST_USER, TEST_PASS)

        self.mock_ssh.return_value.connect.assert_called_once_with(TEST_HOST,
                                                                   port=TEST_HOST_PORT,
                                                                   username=TEST_USER,
                                                                   password=TEST_PASS)

    def test_close(self):
        with Channel(TEST_HOST, TEST_HOST_PORT):
            pass

        self.mock_ssh.return_value.close.assert_called_once_with()

    def test_run(self):
        cmd = self.channel.run(['some', 'test', 'command'])

        self.mock_ssh.return_value.exec_command.assert_called_once_with('some test command')

        self.assertEqual(cmd.stdin.read(), TEST_STDIN)
        self.assertEqual(cmd.stdout.read(), TEST_STDOUT)
        self.assertEqual(cmd.stderr.read(), TEST_STDERR)
