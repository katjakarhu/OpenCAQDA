import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Sequence, UniqueConstraint, Text, DateTime, \
    func, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr

from ocaqda.data.enums.coderelationshipenum import CodeRelationshipEnum

Base = declarative_base()


class TimestampColumnMixin(object):
    created = Column(DateTime, default=func.now(), nullable=False)
    updated = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class UserColumnMixin(object):
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


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
    name = Column(String, unique=True)
    description = Column(String)
    status = Column(String)
    url = Column(String)


class DataFile(Base, TimestampColumnMixin, UserColumnMixin):
    __tablename__ = "data_files"
    file_id = Column(Integer, Sequence('file_id_seq'), primary_key=True)
    display_name = Column(String)
    original_name = Column(String)
    file_extension = Column(String)
    file_as_text = Column(Text)
    file_content = Column(LargeBinary)
    code_id = Column(Integer, ForeignKey('codes.code_id'))  # you can code files as well
    project_id = Column(Integer, ForeignKey("projects.project_id"))


class Code(Base, TimestampColumnMixin, UserColumnMixin):
    __tablename__ = "codes"
    code_id = Column(Integer, Sequence('code_id_seq'), primary_key=True)
    name = Column(String)
    notes = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.project_id"))


class CodeRelationship(Base, TimestampColumnMixin, UserColumnMixin):
    """Relationships between codes. Note that Parent relationship (label = 'parent') is a special case that is used when displaying
    codes in the AnalysisTab on the UI."""
    __tablename__ = "code_connections"
    connection_id = Column(Integer, primary_key=True)
    type = Column(Enum(CodeRelationshipEnum))
    label = Column(String)
    from_code_id = Column(Integer, ForeignKey("codes.code_id"))
    to_code_id = Column(Integer, ForeignKey("codes.code_id"))
    has_direction = Column(Boolean)
    __table_args__ = (UniqueConstraint('from_code_id', 'to_code_id', 'label', name='_from_to_label_uc'),)


class CodedText(Base, TimestampColumnMixin, UserColumnMixin):
    __tablename__ = "coded_texts"
    coded_text_id = Column(Integer, Sequence('coded_text_id_seq'), primary_key=True)
    text = Column(Text)
    position = Column(Integer)  # start position of text in file, with len(text) you can get the end position
    code_id = Column(Integer, ForeignKey("codes.code_id"))
    file_id = Column(Integer, ForeignKey("data_files.file_id"))
