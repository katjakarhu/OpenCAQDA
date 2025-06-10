"""
Handles everything within the project: CRUD operations for files, codes and notes


"""

from pathlib import Path

from ocaqda.data.database.databaseconnectivity import DatabaseConnectivity
from ocaqda.data.models import Project, Code, DataFile, FileContent, CodedText
from ocaqda.services.userservice import UserService



def get_file_content_from_db(file_as_bytes):
    session = DatabaseConnectivity().create_new_db_session()
    result = session.query(FileContent).filter(FileContent.content == file_as_bytes).one_or_none()
    session.close()
    return result


class ProjectService:
    def __init__(self, name):
        self.current_project = None
        self.name = name
        self.load_or_create_project(name)

    def create_project(self, name):
        user = UserService().user
        session = DatabaseConnectivity().create_new_db_session()

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
        session = DatabaseConnectivity().create_new_db_session()

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
        session = DatabaseConnectivity().create_new_db_session()

        for name in code_list:
            code = Code()
            code.name = name
            code.project_id = self.current_project.project_id
            code.created_by = UserService().user.user_id
            code.updated_by = UserService().user.user_id
            session.add(code)

        session.commit()
        session.close()

    def get_project_files(self):
        session = DatabaseConnectivity().create_new_db_session()
        result = session.query(DataFile).filter(DataFile.project_id == self.current_project.project_id).all()

        session.close()
        return result

    def save_files(self, file_list):
        session = DatabaseConnectivity().create_new_db_session()
        user = UserService().user

        for file_path in file_list:
            file_path = Path(file_path)
            if file_path.exists():
                # read file
                new_file = DataFile()
                new_file.display_name = file_path.name
                new_file.url = str(file_path.absolute())
                new_file.file_extension = file_path.suffix
                self.add_file_content(file_path, new_file, session, user)
                new_file.created_by = user.user_id
                new_file.updated_by = user.user_id
                new_file.project_id = self.current_project.project_id
                session.add(new_file)

        session.commit()
        session.close()

    def add_file_content(self, file_path, new_file, session, user):
        f = open(file_path, 'rb')
        file_as_bytes = f.read()
        content_from_db = get_file_content_from_db(file_as_bytes)
        if content_from_db is not None:
            session.add(content_from_db)
            new_file.file_content = content_from_db
        else:
            content = FileContent()
            content.content = file_as_bytes
            content.created_by = user.user_id
            content.updated_by = user.user_id
            new_file.file_content = content
            session.add(content)

        f.close()

        f = open(file_path, 'r')
        if new_file.file_extension == ".txt":
            new_file.file_as_text = f.read()
        elif new_file.file_extension == ".pdf":
            from pypdf import PdfReader

            # creating a pdf reader object
            reader = PdfReader(str(file_path))

            text_content = ""
            for page in reader.pages:
                text = page.extract_text()
                text_content += text
            new_file.file_as_text = text_content
            reader.close()
        f.close()

    def get_text_from_file(self, file_path, new_file):
        pass

    def delete_file_from_db(self, file):
        session = DatabaseConnectivity().create_new_db_session()

        session.delete(file)
        session.commit()
        session.close()

    def get_project_codes(self):
        session = DatabaseConnectivity().create_new_db_session()
        result = session.query(Code).filter(Code.project_id == self.current_project.project_id).all()
        session.close()
        return result

    def save_coded_text(self, coded_text):
        session = DatabaseConnectivity().create_new_db_session()
        session.add(coded_text)
        session.commit()
        session.close()

    def get_coded_texts(self, data_file_id, name):
        session = DatabaseConnectivity().create_new_db_session()
        result = session.query(CodedText).filter(CodedText.data_file_id == data_file_id).all()
        session.close()
        return result

    def get_code(self, code_id):
        session = DatabaseConnectivity().create_new_db_session()
        result = session.query(Code).filter(Code.code_id == code_id).one()
        session.close()
        return result

    def load_binary_file_content(self, datafile):
        session = DatabaseConnectivity().create_new_db_session()
        session.add(datafile)
        result = datafile.file_content
        session.close()
        return result.content

def populate_projects():
    session = DatabaseConnectivity().create_new_db_session()

    existing_projects = session.query(Project).all()
    list_of_projects = []
    for existing_project in existing_projects:
        list_of_projects.append(existing_project.name)
    session.commit()
    session.close()
    return list_of_projects
