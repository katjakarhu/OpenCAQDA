""""
Provides access to the current user object
"""

from ocaqda.database import DatabaseConnectivity
from ocaqda.data.models import User
from ocaqda.services.configurationservice import ConfigurationService
from ocaqda.utils.singleton import Singleton


def get_user_from_database(username):
    session = DatabaseConnectivity().create_new_db_session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user


class UserService(metaclass=Singleton):
    def __init__(self):
        self.user = get_user_from_database(ConfigurationService().username)

        print("User loaded.")
