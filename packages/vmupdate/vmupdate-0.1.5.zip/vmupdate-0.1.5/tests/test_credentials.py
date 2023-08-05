import unittest

import mock

from vmupdate.config import config
from vmupdate.credentials import get_credentials, get_run_as_elevated

from tests.context import get_data_path


class CredentialsTestCase(unittest.TestCase):
    def setUp(self):
        config.load(get_data_path('testconfig.yaml'))

    @mock.patch('keyring.get_password')
    def test_get_credentials(self, keyring_mock):
        def keyring_get_password(service_name, username):
            if service_name == 'Test Machine 2' and username == 'testuser2':
                return 'keyringpass1'
            elif service_name == 'vmupdate':
                return 'defaultkeyringpass'

        keyring_mock.side_effect = keyring_get_password

        user, password = get_credentials('Default Test Machine')

        self.assertEqual(user, 'defaulttestuser')
        self.assertEqual(password, 'defaultkeyringpass')

        user, password = get_credentials('Test Machine 1')

        self.assertEqual(user, 'testuser1')
        self.assertEqual(password, 'testpass1')

        user, password = get_credentials('Test Machine 2')

        self.assertEqual(user, 'testuser2')
        self.assertEqual(password, 'keyringpass1')

        user, password = get_credentials('Test Machine 3')

        self.assertEqual(user, 'testuser3')
        self.assertEqual(password, 'defaultkeyringpass')

        user, password = get_credentials('Test Machine 4')

        self.assertEqual(user, 'testuser4')
        self.assertEqual(password, 'defaulttestpass')

    def test_get_run_as_elevated(self):
        self.assertFalse(get_run_as_elevated('Default Test Machine'))
        self.assertTrue(get_run_as_elevated('Test Machine 1'))
        self.assertFalse(get_run_as_elevated('Test Machine 2'))
