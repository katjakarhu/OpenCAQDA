import sys

from PySide6.QtWidgets import QApplication
from sqlalchemy_utils import database_exists, create_database

from data.database.databaseconnection import DatabaseEngine
from data.models import Base
from ui.mainqawindow import MainQAWindow
from ui.startupdialog import StartUpDialog

TEST_MODE = False


def initialize_database():
    """
        Initializes the database. If database does not exist, it is created.
        In test mode all tables are dropped and re-created
    """
    db_engine = DatabaseEngine()
    if not database_exists(db_engine.url):
        create_database(db_engine.url)

    if TEST_MODE:
        Base.metadata.drop_all(db_engine)
        Base.metadata.create_all(db_engine)


def open_project_window(name):
    # Open a new QMainWindow instance for the selected project
    main_window = MainQAWindow()
    main_window.set_project(name)
    main_window.initialize_layout()
    main_window.show()
    main_window.raise_()


def open_project_window(item):
    # Open a new QMainWindow instance for the selected project
    MainQAWindow().show()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage: python main.py [options]")
            print("Options:")
            print("--help Shows this message")
            print("--version Shows version")
            print("--test Test mode where database tables are dropped and recreated")
        elif sys.argv[1] == "--test":
            print("WARNING: Database has been recreated")
            TEST_MODE = True

    initialize_database()

    app = QApplication(sys.argv)
    dialog = StartUpDialog()
    dialog.show()
    if dialog.exec():
        w = MainQAWindow(dialog.selected_project_name)

        w.showMaximized()

    sys.exit(app.exec())
