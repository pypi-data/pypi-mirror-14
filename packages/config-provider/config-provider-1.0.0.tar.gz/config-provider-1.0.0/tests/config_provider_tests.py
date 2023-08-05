__author__ = 'bcullen'

import unittest
from config_provider.config_provider import ConfigProvider


class TestConfigProvider(unittest.TestCase):
    """
    Test ability to get config JSON from DynamoDB
    """

    @classmethod
    def setUpClass(self):
        self._config_provider = ConfigProvider('unit_test')

    # Test lookup code without integration to persistent storage
    def test_val_in_stubbed_dictionary(self):
        test_dict = {"username": "unittestuser"}
        self._config_provider._resources['unit_test'] = test_dict

        val = self._config_provider['unit_test']['username']
        self.assertEqual(val, 'unittestuser')

    def test_env_doesnt_exist(self):
        default_config_provider = ConfigProvider('foo-env-doesnt-exist')
        username = default_config_provider['unit_test']['username']
        self.assertEqual(username, 'testuser')
        password = default_config_provider['unit_test']['password']
        self.assertEqual(password, 'testpass')

    def test_env_override(self):
        username = self._config_provider['unit_test']['username']
        self.assertEqual(username, 'testuser')
        password = self._config_provider['unit_test']['password']
        self.assertEqual(password, 'envtestpass')

    def helper_test_resource_not_found(self):
        return self._config_provider['foo-doesnt-exist']['username']

    def test_resource_not_found(self):
        self.assertRaises(KeyError, self.helper_test_resource_not_found)

    def helper_test_attribute_not_found(self):
        return self._config_provider['unit_test']['bar-doesnt-exist']

    def test_attribute_not_found(self):
        self.assertRaises(KeyError, self.helper_test_attribute_not_found)

    def test_creation_with_bad_env_name(self):
        c = ConfigProvider("foo_barrr")
        self.assertEqual(c["unit_test"]["password"], "testpass")

    def test_creation_with_good_env_name(self):
        c = ConfigProvider("unit_test")
        self.assertEqual(c["unit_test"]["password"], "envtestpass")

    def tearDown(self):
        pass


def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestConfigProvider)
