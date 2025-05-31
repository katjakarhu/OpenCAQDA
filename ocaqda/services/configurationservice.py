from pathlib import Path

import yaml

from ocaqda.utils.constants import CONFIGURATION_FILE_NAME
from ocaqda.utils.singleton import Singleton


class ConfigurationService(metaclass=Singleton):
    def __init__(self):
        data = load_configuration()
        self.username = data['username']
        self.database_url = data['database_url']

        if self.username == '' or self.database_url == '':
            raise ValueError("Configuration not set")

        print("Configuration loaded.")


def load_configuration():
    home_dir = Path.home()
    conf_file_path = Path(CONFIGURATION_FILE_NAME)
    print(conf_file_path.absolute())
    if conf_file_path.exists():
        print("Configuration file found. " + str(conf_file_path.absolute()))
        file = open(conf_file_path, 'r')
        app_configuration = yaml.safe_load(file)
        file.close()
    else:
        settings_data = dict(username='', database_url='sqlite:///opencaqda-db.db')
        file = open(conf_file_path, 'w')
        yaml.safe_dump(settings_data, file)
        file.close()
        file = open(conf_file_path, 'r')
        app_configuration = yaml.safe_load(file)
        file.close()

    # TODO store and fetch password from keyring
    return app_configuration
