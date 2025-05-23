from importlib import resources

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

DB_URL = f"sqlite:///oqcoder.db"

class DatabaseEngine(Engine):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = create_engine(DB_URL)
        return cls.instance

#db_engine = DatabaseEngine()
#db_session = Session(bind=db_engine)

#with resources.path(
#        "project.data", "oqcoder.db"
#    ) as sqlite_filepath:
#       self = create_engine(f"sqlite:///{sqlite_filepath}")


# create a configured "Session" class
#Session = sessionmaker(bind=some_engine)

# create a Session
#session = Session()