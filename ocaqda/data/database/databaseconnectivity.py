from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ocaqda.utils.singleton import Singleton


class DatabaseConnectivity(metaclass=Singleton):
    def __init__(self, *args):
        if len(args) > 0:
            db_url = args[0]
            print(db_url)
            self.engine = create_engine(eval("f'{}'".format(db_url)))


    def create_new_db_session(self):
        database_session = sessionmaker(bind=self.engine)
        session = database_session()
        return session


# db_engine = DatabaseEngine()
# db_session = Session(bind=db_engine)

# with resources.path(
#        "project.data", "oqcoder.db"
#    ) as sqlite_filepath:
#       self = create_engine(f"sqlite:///{sqlite_filepath}")


# create a configured "Session" class
# Session = sessionmaker(bind=some_engine)

# create a Session
# session = Session()
