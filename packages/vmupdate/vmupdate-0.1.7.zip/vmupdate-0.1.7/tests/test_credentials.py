from vmupdate.config import config
from vmupdate.credentials import get_credentials, get_run_as_elevated

from tests.case import TestCase
from tests.constants import *
from tests.context import get_data_path
from tests.mocks import keyring_get_password


class CredentialsTestCase(TestCase):
    def setUp(self):
        config.load(get_data_path('testconfig.yaml'))

        self.mock_patch_get_password = self.add_mock('keyring.get_password', autospec=True,
                                                     side_effect=keyring_get_password)

    def test_default_password(self):
        user, password = get_credentials('Test Machine 4')

        self.assertEqual(user, 'testuser4')
        self.assertEqual(password, 'defaulttestpass')

    def test_default_keyring(self):
        user, password = get_credentials('Default Test Machine')

        self.assertEqual(user, 'defaulttestuser')
        self.assertEqual(password, TEST_DEFAULT_KEYRING_PASS)

    def test_machine_credentials(self):
        user, password = get_credentials('Test Machine 1')

        self.assertEqual(user, 'testuser1')
        self.assertEqual(password, 'testpass1')

    def test_machine_keyring(self):
        user, password = get_credentials('Test Machine 2')

        self.assertEqual(user, 'testuser2')
        self.assertEqual(password, TEST_KEYRING_PASS)

    def test_machine_default_keyring(self):
        user, password = get_credentials('Test Machine 3')

        self.assertEqual(user, 'testuser3')
        self.assertEqual(password, TEST_DEFAULT_KEYRING_PASS)

    def test_get_run_as_elevated(self):
        self.assertFalse(get_run_as_elevated('Default Test Machine'))
        self.assertTrue(get_run_as_elevated('Test Machine 1'))
        self.assertFalse(get_run_as_elevated('Test Machine 2'))
