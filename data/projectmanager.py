from json import loads

from PySide6.scripts.pyside_tool import project
from data.database.databaseconnection import DatabaseEngine
from data.models import Project
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


class ProjectManager:
    def __init__(self, name):
        self.current_project = None
        self.db_engine = DatabaseEngine()
        self.name = name
        self.load_or_create_project(name)

    def save_project(self):
        pass

    def create_project(self, name):
        # Create a configured "Session" class
        database_session = sessionmaker(bind=self.db_engine)

        # Create a Session
        session = database_session()

        proj = Project(name=name)
        session.add(proj)
        session.commit()

        self.current_project = session.query(Project).filter(Project.name == name).one()

    def load_or_create_project(self, name):
        # Create a configured "Session" class
        session_class = sessionmaker(bind=self.db_engine)

        # Create a Session
        session = session_class()

        proj = session.query(Project).filter(Project.name == name).one_or_none()

        if proj is None:
            self.create_project(name)
        else:
            self.current_project = proj

    def export_project(self):
        pass

    def import_project(self):
        pass
