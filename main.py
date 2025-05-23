import sys

from data.database.databaseconnection import DatabaseEngine
from data.models import Project, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from ui.startupdialog import StartUpDialog


def initialize_database():
    db_engine = DatabaseEngine()
    if not database_exists(db_engine.url):
        create_database(db_engine.url)
    Base.metadata.drop_all(db_engine)
    Base.metadata.create_all(db_engine)


if __name__ == "__main__":
    initialize_database()

    app = QApplication(sys.argv)
    dialog = StartUpDialog()
    dialog.show()
    sys.exit(app.exec())
