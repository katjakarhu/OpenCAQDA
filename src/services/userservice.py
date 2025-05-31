from sqlalchemy.orm import sessionmaker

from src.data.database.databaseengine import DatabaseEngine
from src.data.models import User
from src.services.configurationservice import ConfigurationService
from src.utils.singleton import Singleton


def get_user_from_database(username):
    database_session = sessionmaker(bind=DatabaseEngine().engine)
    session = database_session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user


class UserService(metaclass=Singleton):
    def __init__(self):
        self.user = get_user_from_database(ConfigurationService().username)

        print("User loaded.")
