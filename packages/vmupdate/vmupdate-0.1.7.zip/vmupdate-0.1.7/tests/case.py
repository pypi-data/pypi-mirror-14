import unittest

import mock


class TestCase(unittest.TestCase):
    def add_mock(self, *args, **kwargs):
        patcher = mock.patch(*args, **kwargs)
        self.addCleanup(patcher.stop)

        return patcher.start()
