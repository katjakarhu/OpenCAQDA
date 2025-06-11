"""
Main application, loads configuration from opencaqda-settings.yaml,
initializes database (if specified or does not exist),
and displays StartUpDialog
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from sqlalchemy_utils import create_database

from data.models import Base
from ocaqda.database.databaseconnectivity import DatabaseConnectivity
from ocaqda.services.configurationservice import load_configuration
from ocaqda.ui.mainview.mainqawindow import MainQAWindow
from ocaqda.ui.startupdialog import StartUpDialog


def initialize_database(db_url, recreate=False):
    """
        Initializes the database. If database does not exist, it is created.
        In test mode all tables are dropped and re-created
    """
    database_path = Path(db_url[10])

    if recreate and database_path.exists():
        database_path.unlink()

    if not database_path.exists():
        db_engine = DatabaseConnectivity(db_url)
        create_database(db_engine.engine.url)
        Base.metadata.create_all(db_engine.engine)

    else:
        # Initialize the singleton
        DatabaseConnectivity(db_url)


if __name__ == "__main__":

    recreate_database = False

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Usage: python main.py [options]")
            print("Options:")
            print("--help Shows this message")
            print("--version Shows version")
            print("--recreate-database (WARNING) Database tables are dropped and recreated. Destroys all data.")
        elif sys.argv[1] == "--recreate-database":
            print("WARNING: Database has been recreated")
            recreate_database = True

    # TODO: if DB location is not set, ask user (I have a file, OR I want to create a new DB)

    config = load_configuration()
    database_url = config['database_url']

    initialize_database(database_url, recreate_database)

    app = QApplication(sys.argv)
    dialog = StartUpDialog()
    dialog.show()
    if dialog.exec():
        w = MainQAWindow(dialog.selected_project_name)

        w.showMaximized()

    sys.exit(app.exec())
