"""
Tests for configurationservice.py
"""

import os
import unittest
from pathlib import Path

import yaml

from ocaqda.services.configurationservice import ConfigurationService
from ocaqda.utils.constants import CONFIGURATION_FILE_NAME


# noinspection PyMethodMayBeStatic
class NoConfigurationFileTest(unittest.TestCase):
    def setUp(self):
        if Path(CONFIGURATION_FILE_NAME).exists():
            os.remove(CONFIGURATION_FILE_NAME)

    def tearDown(self):
        if Path(CONFIGURATION_FILE_NAME).exists():
            os.remove(CONFIGURATION_FILE_NAME)

    def test_configuration_service_is_none(self):
        conf_service = None
        try:
            conf_service = ConfigurationService()
        except Exception as e:
            assert str(e) == "Configuration not set"

        assert conf_service is None


# noinspection PyMethodMayBeStatic
class ConfigurationFileExistsTest(unittest.TestCase):
    def setUp(self):
        if Path(CONFIGURATION_FILE_NAME).exists():
            os.remove(CONFIGURATION_FILE_NAME)
        conf_file_path = Path(CONFIGURATION_FILE_NAME)
        settings_data = dict(username='test', database_url='sqlite://test.db')
        file = open(conf_file_path, 'w')
        yaml.safe_dump(settings_data, file)
        file.close()

    def tearDown(self):
        os.remove(CONFIGURATION_FILE_NAME)

    def test_configurationValuesArePresentTest(self):
        conf_service = ConfigurationService()
        assert conf_service.username == 'test'
        assert conf_service.database_url == 'sqlite://test.db'

    def test_isSingleton(self):
        conf_service = ConfigurationService()
        conf_service2 = ConfigurationService()

        assert conf_service is conf_service2
