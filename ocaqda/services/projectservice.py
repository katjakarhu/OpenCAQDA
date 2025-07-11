"""
Handles everything within the project: CRUD operations for files, codes and notes


"""

from pathlib import Path

from ocaqda.data.enums.coderelationshipenum import CodeRelationshipEnum
from ocaqda.data.models import Project, Code, DataFile, FileContent, CodedText, CodeRelationship, Note
from ocaqda.database.databaseconnectivity import DatabaseConnectivity
from ocaqda.services.userservice import UserService
from ocaqda.utils.pdfutils import convert_pdf_to_html


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
            code = self.set_audit_data(code)
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
                new_file = self.set_audit_data(new_file)
                session.add(new_file)
                session.commit()

        session.close()

    def add_file_content(self, file_path, new_file, session, user):
        f = open(file_path, 'rb')
        file_as_bytes = f.read()
        content_from_db = get_file_content_from_db(file_as_bytes)
        if content_from_db is not None:
            new_file.file_content_id = content_from_db.file_content_id
        else:
            content = FileContent()
            content.content = file_as_bytes
            content.created_by = user.user_id
            content.updated_by = user.user_id
            new_file.file_content = content
            session.add(content)

        f.close()

        f = open(file_path, 'r')
        if new_file.file_extension in (".txt", ".html", ".md"):
            new_file.file_as_text = f.read()
        elif new_file.file_extension == ".pdf":

            result = convert_pdf_to_html(str(file_path))
            new_file.file_as_text = result
        f.close()

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
        coded_text = self.set_audit_data(coded_text)

        session.add(coded_text)
        session.commit()
        session.close()

    def get_coded_texts_for_current_project(self):
        session = DatabaseConnectivity().create_new_db_session()
        result = session.query(CodedText).where(CodedText.project_id == self.current_project.project_id).all()
        session.close()
        return result

    def get_coded_texts_by_code_id(self, id):
        session = DatabaseConnectivity().create_new_db_session()
        result = session.query(CodedText).where(CodedText.code_id == id).all()
        session.close()
        return result

    def get_coded_texts_by_file(self, data_file_id, name):
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

    def update_code_parent_child_relationships(self, code_relationships):
        """
        Delete-insert operation: recreates all parent-child relationships after deleting old ones
        """
        session = DatabaseConnectivity().create_new_db_session()

        parent_child_relationships = session.query(CodeRelationship).filter(
            (CodeRelationship.project_id == self.current_project.project_id) &
            (CodeRelationship.type == CodeRelationshipEnum.PARENT)).all()

        for rel in parent_child_relationships:
            session.delete(rel)

        self.add_new_relationships(code_relationships, session)

        session.commit()
        session.close()

    def add_new_relationships(self, code_relationships, session):
        parent_child_list = []
        for parent_item in code_relationships.keys():
            parent_id = parent_item.code_id
            children = code_relationships[parent_item]
            if isinstance(children, Code):
                child_ids = [children.code_id]
            else:
                child_ids = [x.code_id for x in children]

            for child_id in child_ids:
                r = CodeRelationship()
                r.from_code_id = parent_id
                r.to_code_id = child_id
                r.type = CodeRelationshipEnum.PARENT
                r = self.set_audit_data(r)
                parent_child_list.append(r)

        if len(parent_child_list) > 0:
            session.add_all(parent_child_list)

    def get_parent_child_relationships(self):
        session = DatabaseConnectivity().create_new_db_session()
        result = session.query(CodeRelationship.from_code_id, CodeRelationship.to_code_id).filter(
            CodeRelationship.type == CodeRelationshipEnum.PARENT).all()
        session.close()
        return result

    def load_note_for_code(self, id):
        session = DatabaseConnectivity().create_new_db_session()
        code = session.query(Code).where(
            Code.project_id == self.current_project.project_id).filter(Code.code_id == id).one()
        note = code.note
        session.close()
        return note

    def load_note_for_file(self, id):
        session = DatabaseConnectivity().create_new_db_session()
        file = session.query(DataFile).where(
            DataFile.project_id == self.current_project.project_id).filter(DataFile.data_file_id == id).one()
        note = file.note
        session.close()
        return note

    def save_note_for_code(self, id, note_text):
        session = DatabaseConnectivity().create_new_db_session()
        code = session.query(Code).where(
            Code.project_id == self.current_project.project_id).filter(Code.code_id == id).one()
        if code.note is None:
            note = Note()
            note.text = note_text
            note = self.set_audit_data(note)
            code.note = note
        else:
            code.note.text = note_text
            code.note.updated_by = UserService().user.user_id

        session.commit()
        session.close()

    def save_note_for_file(self, id, note_text):
        session = DatabaseConnectivity().create_new_db_session()
        file = session.query(DataFile).where(
            DataFile.project_id == self.current_project.project_id).filter(DataFile.data_file_id == id).one()
        if file.note is None:
            note = Note()
            note.text = note_text
            note.created_by = UserService().user.user_id
            note.updated_by = UserService().user.user_id
            file.note = note
        else:
            file.note.text = note_text
            file.note.updated_by = UserService().user.user_id

        session.commit()
        session.close()

    def get_code_from_coded_text(self, coded_text):
        session = DatabaseConnectivity().create_new_db_session()
        session.add(coded_text)
        code = coded_text.code
        session.close()
        return code

    def delete_coded_text(self, coded_text):
        session = DatabaseConnectivity().create_new_db_session()
        session.delete(coded_text)
        session.commit()
        session.close()

    def get_file_by_id(self, file_id):
        session = DatabaseConnectivity().create_new_db_session()
        result = session.query(DataFile).where(DataFile.data_file_id == file_id).one()

        session.close()
        return result

    def set_audit_data(self, entity):
        entity.created_by = UserService().user.user_id
        entity.updated_by = UserService().user.user_id
        entity.project_id = self.current_project.project_id
        return entity


def populate_projects():
    session = DatabaseConnectivity().create_new_db_session()

    existing_projects = session.query(Project).all()
    list_of_projects = []
    for existing_project in existing_projects:
        list_of_projects.append(existing_project.name)
    session.commit()
    session.close()
    return list_of_projects
