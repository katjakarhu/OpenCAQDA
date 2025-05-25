from enum import unique

from data.database.databaseconnection import DatabaseEngine
from sqlalchemy import Column, Integer, String, ForeignKey, Table, LargeBinary, Sequence, UniqueConstraint, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True)
    color = Column(String)


class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, Sequence('project_id_seq'), primary_key=True)
    name = Column(String, unique=True)
    url = Column(String)


class DataFile(Base):
    __tablename__ = "data_files"
    file_id = Column(Integer, Sequence('file_id_seq'), primary_key=True)
    display_name = Column(String)
    name = Column(String)
    file_extension = Column(String)
    file_as_text = Column(Text)
    file_content = Column(LargeBinary)  # TODO: maybe store files in the file system instead
    url = Column(String)  # file location on the file system
    code_id = Column(Integer, ForeignKey('codes.code_id'))  # you can code files as well
    project_id = Column(Integer, ForeignKey("projects.project_id"))


class Code(Base):
    __tablename__ = "codes"
    code_id = Column(Integer, Sequence('code_id_seq'), primary_key=True)
    name = Column(String)
    notes = Column(String)
    project_id = Column(Integer, ForeignKey("projects.project_id"))
    # Parent is for grouping codes together
    parent_id = Column(Integer, ForeignKey("codes.code_id"))


class CodeConnection(Base):
    __tablename__ = "code_connections"
    connection_id = Column(Integer, primary_key=True)
    code_id = Column(Integer, ForeignKey("codes.code_id"))
    sibling_id = Column(Integer, ForeignKey("codes.code_id"))
    __table_args__ = (UniqueConstraint('code_id', 'sibling_id', name='_code_sibling_uc'),)


class CodedText(Base):
    __tablename__ = "coded_texts"
    coded_text_id = Column(Integer, Sequence('coded_text_id_seq'), primary_key=True)
    text = Column(String)
    position = Column(Integer)  # start position of text in file, with len(text) you can get the end position
    code_id = Column(Integer, ForeignKey("codes.code_id"))
    file_id = Column(Integer, ForeignKey("data_files.file_id"))
