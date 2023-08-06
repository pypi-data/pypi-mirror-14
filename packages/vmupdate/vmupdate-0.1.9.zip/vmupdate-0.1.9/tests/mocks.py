import mock
import paramiko

from vmupdate.virtualizers import Virtualizer

from tests.constants import *


def keyring_get_password(service_name, username):
    if service_name == 'Test Machine 2' and username == 'testuser2':
        return TEST_KEYRING_PASS
    elif service_name == 'vmupdate':
        return TEST_DEFAULT_KEYRING_PASS


def get_mock_ssh_client():
    mock_ssh = mock.Mock(spec=paramiko.SSHClient)

    mock_stdin = create_mock_ssh_channel_file(TEST_STDIN)
    mock_stdout = create_mock_ssh_channel_file(TEST_STDOUT)
    mock_stderr = create_mock_ssh_channel_file(TEST_STDERR)

    mock_ssh.return_value.exec_command.return_value = (mock_stdin, mock_stdout, mock_stderr)

    return mock_ssh


def create_mock_ssh_channel_file(out):
    mock_channel_file = mock.MagicMock(spec=paramiko.ChannelFile)

    mock_channel_file.read.return_value = out
    mock_channel_file.readline.return_value = out
    mock_channel_file.readlines.return_value = [out]
    mock_channel_file.__iter__.return_value = iter([out])

    mock_channel = mock.Mock(spec=paramiko.Channel)

    mock_channel.recv_exit_status.return_value = 0
    mock_channel_file.channel = mock_channel

    return mock_channel_file


def get_mock_virtualizer():
    mock_virt = mock.Mock(spec=Virtualizer)

    mock_virt.get_vm_os.return_value = TEST_OS
    mock_virt.get_vm_status.return_value = TEST_STATUS
    mock_virt.get_ssh_info.return_value = (TEST_HOST, TEST_HOST_PORT)
    mock_virt.enable_ssh.return_value = TEST_EXITCODE
    mock_virt.list_vms.return_value = [('Test Machine 1', None), ('Test Machine 2', None),
                                       ('Test Machine 3', None), ('Test Machine 4', None)]

    return mock_virt
