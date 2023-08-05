import unittest

from vmupdate.config import config

from tests.context import get_data_path


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        config.load()

    def test_general(self):
        self.assertEqual(config.general.wait_after_start, 30)
        self.assertEqual(config.general.wait_before_stop, 10)

    def test_credentials(self):
        self.assertEqual(config.credentials.username, 'root')
        self.assertIsNone(config.credentials.password)
        self.assertTrue(config.credentials.use_keyring)
        self.assertTrue(config.credentials.run_as_elevated)

    def test_network(self):
        self.assertEqual(config.network.ssh.guest_port, 22)
        self.assertEqual(config.network.ssh.host_min_port, 49152)
        self.assertEqual(config.network.ssh.host_max_port, 65535)

    def test_machines(self):
        self.assertNotIn('Test Machine 1', config.machines)
        self.assertNotIn('Test Machine 2', config.machines)


class UserConfigTestCase(unittest.TestCase):
    def setUp(self):
        config.load(get_data_path('testconfig.yaml'))

    def test_general(self):
        self.assertEqual(config.general.wait_after_start, 30)

    def test_credentials(self):
        self.assertEqual(config.credentials.username, 'defaulttestuser')
        self.assertEqual(config.credentials.password, 'defaulttestpass')
        self.assertTrue(config.credentials.use_keyring)
        self.assertFalse(config.credentials.run_as_elevated)

    def test_network(self):
        self.assertEqual(config.network.ssh.guest_port, 33)
        self.assertEqual(config.network.ssh.host_min_port, 49152)
        self.assertEqual(config.network.ssh.host_max_port, 65000)

    def test_machines(self):
        self.assertIn('Test Machine 1', config.machines)
        self.assertEqual(config.machines['Test Machine 1'].username, 'testuser1')
        self.assertEqual(config.machines['Test Machine 1'].password, 'testpass1')

        self.assertIn('Test Machine 2', config.machines)
        self.assertEqual(config.machines['Test Machine 2'].username, 'testuser2')
        self.assertIsNone(config.machines['Test Machine 2'].password)
        self.assertFalse(config.machines['Test Machine 2'].use_keyring)
