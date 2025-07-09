"""
Entities stored in database
"""

import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Sequence, UniqueConstraint, Text, DateTime, \
    func, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr, relationship, backref

from ocaqda.data.enums.coderelationshipenum import CodeRelationshipEnum

Base = declarative_base()


class TimestampColumnMixin:
    created = Column(DateTime, default=func.now(), nullable=False)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()


class UserColumnMixin:
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()


class User(Base, TimestampColumnMixin):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    color = Column(String)
    password = Column(Text, nullable=False)
    email = Column(String)

    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password, self.password)
        return self.password == pwhash


class Project(Base, TimestampColumnMixin, UserColumnMixin):
    __tablename__ = "projects"
    project_id = Column(Integer, Sequence('project_id_seq'), primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    status = Column(String)
    url = Column(String)
    data_files = relationship("DataFile", back_populates="project")

    note_id = Column(Integer, ForeignKey("notes.note_id"), nullable=True)
    note = relationship("Note", backref=backref("Project", uselist=False))


class DataFile(Base, TimestampColumnMixin, UserColumnMixin):
    __tablename__ = "data_files"
    data_file_id = Column(Integer, Sequence('data_file_id_seq'), primary_key=True)
    display_name = Column(String, nullable=False)
    url = Column(String)
    file_extension = Column(String, nullable=False)
    file_as_text = Column(Text)
    # Store the file content as binary only once, same content can be used in many projects
    file_content_id = Column(Integer, ForeignKey("file_content.file_content_id"), nullable=False)
    file_content = relationship("FileContent", backref=backref("DataFile", uselist=False))

    code_id = Column(Integer, ForeignKey('codes.code_id'))  # you can code files as well

    note_id = Column(Integer, ForeignKey("notes.note_id"), nullable=True)
    note = relationship("Note", backref=backref("DataFile", uselist=False))

    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    project = relationship("Project", back_populates="data_files")
    __table_args__ = (UniqueConstraint('display_name', 'project_id', name='_filename_project_uc'),)


class FileContent(Base, TimestampColumnMixin, UserColumnMixin):
    __tablename__ = "file_content"
    file_content_id = Column(Integer, Sequence('file_content_id_seq'), primary_key=True)
    content = Column(LargeBinary, unique=True, nullable=False)


class Code(Base, TimestampColumnMixin, UserColumnMixin):
    __tablename__ = "codes"
    code_id = Column(Integer, Sequence('code_id_seq'), primary_key=True)
    name = Column(String, nullable=False)
    note_id = Column(Integer, ForeignKey("notes.note_id"), nullable=True)
    note = relationship("Note", backref=backref("Code", uselist=False))
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    __table_args__ = (UniqueConstraint('name', 'project_id', name='_name_project_uc'),)


class CodeRelationship(Base, TimestampColumnMixin, UserColumnMixin):
    """Relationships between codes. Note that Parent relationship (label = 'parent') is a special case that is used when displaying
    codes in the code tab on the UI."""
    __tablename__ = "code_relationships"
    connection_id = Column(Integer, primary_key=True)
    type = Column(Enum(CodeRelationshipEnum), nullable=False)
    label = Column(String)
    from_code_id = Column(Integer, ForeignKey("codes.code_id"), nullable=False)
    to_code_id = Column(Integer, ForeignKey("codes.code_id"), nullable=False)
    has_direction = Column(Boolean)  # this is unnecessary, remove

    note_id = Column(Integer, ForeignKey("notes.note_id"), nullable=True)
    note = relationship("Note", backref=backref("CodeRelationship", uselist=False))

    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    __table_args__ = (UniqueConstraint('from_code_id', 'to_code_id', 'label', name='_from_to_label_uc'),)


class CodedText(Base, TimestampColumnMixin, UserColumnMixin):
    __tablename__ = "coded_texts"
    coded_text_id = Column(Integer, Sequence('coded_text_id_seq'), primary_key=True)
    text = Column(Text, nullable=False)
    start_position = Column(Integer,
                            nullable=False)  # start position of text in file, with len(text) you can get the end position
    end_position = Column(Integer,
                          nullable=False)  # start position of text in file, with len(text) you can get the end position
    code_id = Column(Integer, ForeignKey("codes.code_id"), nullable=False)
    code = relationship("Code", backref=backref("CodedText", uselist=False))

    data_file_id = Column(Integer, ForeignKey("data_files.data_file_id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)


class Note(Base, TimestampColumnMixin, UserColumnMixin):
    __tablename__ = "notes"
    note_id = Column(Integer, Sequence('note_id_seq'), primary_key=True)
    text = Column(Text, nullable=False)
