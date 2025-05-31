from sqlalchemy.orm import sessionmaker

from src.data.database.databaseengine import DatabaseEngine
from src.data.models import Project, Code
from src.services.userservice import UserService


class ProjectService:
    def __init__(self, name):
        self.current_project = None
        self.db_engine = DatabaseEngine().engine
        self.name = name
        self.load_or_create_project(name)

    def create_new_db_session(self):
        database_session = sessionmaker(bind=self.db_engine)
        session = database_session()
        return session

    def create_project(self, name):
        user = UserService().user
        print(user.username + " created " + user.user_id)
        session = self.create_new_db_session()

        proj = Project(name=name)
        proj.created_by = user.user_id
        proj.updated_by = user.user_id
        session.add(proj)
        session.commit()

        self.current_project = session.query(Project).filter(Project.name == name).one()

        session.close()

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

        session.close()

    def export_project(self):
        pass

    def import_project(self):
        pass

    def save_code(self, code_name):
        self.save_codes([code_name])

    def save_codes(self, code_list):
        session = self.create_new_db_session()

        for name in code_list:
            code = Code()
            code.name = name
            code.project_id = self.current_project.project_id
            session.add(code)

        session.commit()
        session.close()

    def save_files(self, file_list):
        pass
