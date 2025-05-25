from sqlalchemy.orm import sessionmaker

from data.database.databaseconnection import DatabaseEngine
from data.models import Project, Code


class ProjectManager:
    def __init__(self, name):
        self.current_project = None
        self.db_engine = DatabaseEngine()
        self.name = name
        self.load_or_create_project(name)

    def create_new_db_session(self):
        database_session = sessionmaker(bind=self.db_engine)
        session = database_session()
        return session

    def create_project(self, name):
        session = self.create_new_db_session()

        proj = Project(name=name)
        session.add(proj)
        session.commit()

        self.current_project = session.query(Project).filter(Project.name == name).one()

    def save_project(self):
        pass

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

    def save_code(self, code_name):
        session = self.create_new_db_session()

        code = Code()
        code.name = code_name
        code.project_id = self.current_project.project_id

        session.add(code)
        session.commit()

    def save_files(self, file_list):
        pass
