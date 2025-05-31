from sqlalchemy import create_engine

from src.utils.singleton import Singleton


class DatabaseEngine(metaclass=Singleton):
    def __init__(self, *args):
        if len(args) > 0:
            db_url = args[0]
            print(db_url)
            self.engine = create_engine(eval("f'{}'".format(db_url)))

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
