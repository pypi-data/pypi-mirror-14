import mock

from vmupdate.config import config
from vmupdate.config import _merge

from tests.case import TestCase
from tests.constants import *
from tests.context import get_data_path


class ConfigTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
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


class UserConfigTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        config.load(config_path=get_data_path('testconfig.yaml'))

    def test_general(self):
        self.assertEqual(config.general.wait_after_start, 30)

    def test_credentials(self):
        self.assertEqual(config.credentials.username, 'defaulttestuser')
        self.assertEqual(config.credentials.password, 'defaulttestpass')
        self.assertTrue(config.credentials.use_keyring)
        self.assertFalse(config.credentials.run_as_elevated)

    def test_network(self):
        self.assertEqual(config.network.ssh.guest_port, TEST_GUEST_PORT)
        self.assertEqual(config.network.ssh.host_min_port, 49152)
        self.assertEqual(config.network.ssh.host_max_port, 65000)

    def test_virtualizers(self):
        self.assertIn(TEST_OS, config.virtualizers)
        self.assertIn(TEST_VIRTUALIZER, config.virtualizers[TEST_OS])
        self.assertListEqual(config.virtualizers[TEST_OS][TEST_VIRTUALIZER], [TEST_VIRTUALIZER_PATH])

    def test_pkgmgrs(self):
        self.assertIn(TEST_OS, config.pkgmgrs)
        self.assertIn(TEST_PKGMGR, config.pkgmgrs[TEST_OS])
        self.assertListEqual(config.pkgmgrs[TEST_OS][TEST_PKGMGR], ['update', 'upgrade'])

    def test_shells(self):
        self.assertIn(TEST_OS, config.shells)
        self.assertEqual(config.shells[TEST_OS], TEST_SHELL)

    def test_machines(self):
        self.assertIn('Test Machine 1', config.machines)
        self.assertEqual(config.machines['Test Machine 1'].username, 'testuser1')
        self.assertEqual(config.machines['Test Machine 1'].password, 'testpass1')

        self.assertIn('Test Machine 2', config.machines)
        self.assertEqual(config.machines['Test Machine 2'].username, 'testuser2')
        self.assertIsNone(config.machines['Test Machine 2'].password)
        self.assertFalse(config.machines['Test Machine 2'].use_keyring)
        self.assertEqual(config.machines['Test Machine 2'].shell, 'TestShell')

    def test_configsection(self):
        self.assertGreater(len(config.machines), 0)
        self.assertEqual(next(config.machines.iterkeys()), config.machines.keys()[0])
        self.assertEqual(next(config.machines.iteritems()), config.machines.items()[0])
        self.assertEqual(next(config.machines.itervalues()), config.machines.values()[0])
        self.assertIsNotNone(iter(config.machines))


class UserLogTestCase(TestCase):
    @mock.patch('logging.config.dictConfig')
    def test_log_dir(self, mock_dict_config):
        config.load(log_dir=TEST_LOG_DIR)

        self.assertTrue(mock_dict_config.called)

        logging_config = mock_dict_config.call_args[0][0]

        self.assert_(logging_config['handlers']['info_file']['filename'].startswith(TEST_LOG_DIR))
        self.assert_(logging_config['handlers']['error_file']['filename'].startswith(TEST_LOG_DIR))


class MergeTestCase(TestCase):
    def test_merge(self):
        a = {
            'key1': 'value1',
            'key2': 'value2',
            'list1': ['item1', 'item2'],
            'list2': ['item3', 'item4'],
            'dict1': {
                'key3': 'value3',
                'key4': 'value4',
                'key5': 'value5',
                'dict2': {
                    'key6': 'value6',
                    'key7': 'value7',
                }
            },
        }
        b = {
            'key2': 'newvalue1',
            'list2': ['newitem1', 'newitem2'],
            'dict1': {
                'key4': None,
                'key5': 'newvalue2',
                'dict2': {
                    'key6': 'newvalue3'
                }
            },
        }

        merged = _merge(a, b)

        self.assertEqual(merged['key1'], 'value1')
        self.assertEqual(merged['key2'], 'newvalue1')
        self.assertListEqual(merged['list1'], ['item1', 'item2'])
        self.assertListEqual(merged['list2'], ['newitem1', 'newitem2'])
        self.assertEqual(merged['dict1']['key3'], 'value3')
        self.assertEqual(merged['dict1']['key4'], 'value4')
        self.assertEqual(merged['dict1']['key5'], 'newvalue2')
        self.assertEqual(merged['dict1']['dict2']['key6'], 'newvalue3')
        self.assertEqual(merged['dict1']['dict2']['key7'], 'value7')
