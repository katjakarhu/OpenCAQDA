import yaml
from PySide6.QtWidgets import QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QPushButton, QInputDialog, \
    QMessageBox, QDialog, QLineEdit, QWidget
from sqlalchemy import exists
from sqlalchemy.orm import sessionmaker

from src.data.database.databaseengine import DatabaseEngine
from src.data.models import Project, User
from src.services.configurationservice import ConfigurationService, load_configuration
from src.ui.newuserdialog import NewUserDialog
from src.utils.constants import CONFIGURATION_FILE_NAME


def can_proceed():
    # TODO also check if user exists in DB
    return ConfigurationService().username != '' and len(ConfigurationService().database_url) > 0


class StartUpDialog(QDialog):
    """
    TODO:
    - set OpenCAQDA location on disk for saving database and additional files
    - fix opening of projects
    """

    def __init__(self):
        super().__init__()
        self.project_list = None
        self.selected_project_name = None
        self.setWindowTitle("OpenCAQDA - Select a project")
        self.setGeometry(100, 100, 400, 400)

        # TODO: if username exists in configuration, perform login (keyring)
        # TODO: if username does not exits, create user and
        if load_configuration()["username"] == '':
            layout = self.create_user_layout()
        else:
            layout = self.create_project_list_layout()

        self.setLayout(layout)

    def create_project_list_layout(self):
        # TODO: load user
        # TODO: create CurrentUserService

        # Layout
        layout = QVBoxLayout()
        # Header label
        header_label = QLabel("OpenCAQDA - Select a project")
        header_style = "font-size: 20px; font-weight: bold;"
        header_label.setStyleSheet(header_style)
        layout.addWidget(header_label)
        # Description text
        description_label = QLabel(
            "Double-click on a project to open it."
        )
        description_label.setWordWrap(True)
        description_label.setMaximumWidth(380)
        description_label.setMinimumHeight(100)
        layout.addWidget(description_label)
        # List widget for projects
        self.project_list = QListWidget()
        self.project_list.setMinimumHeight(100)
        layout.addWidget(self.project_list)
        existing_projects = self.populate_projects()
        self.project_list.addItems(existing_projects)
        # Database location
        database_label = QLabel("Database location: " +
                                ConfigurationService().database_url[10:])
        database_label.setWordWrap(True)
        layout.addWidget(database_label)
        # Buttons layout
        buttons_layout = QHBoxLayout()
        # Add Project Button
        self.add_button = self.create_add_button()
        buttons_layout.addWidget(self.add_button)
        # Edit Database Settings Button, see edit_database_settings method for TODO
        self.edit_db_button = QPushButton("Edit Database Settings")
        self.edit_db_button.clicked.connect(self.edit_database_settings)
        buttons_layout.addWidget(self.edit_db_button)
        layout.addLayout(buttons_layout)
        # Connect project list item click
        self.project_list.itemDoubleClicked.connect(self.quit_dialog)
        return layout

    def create_add_button(self):
        add_button = QPushButton("New Project")
        add_button.clicked.connect(self.add_project)
        add_button.setEnabled(can_proceed())
        return add_button

    def add_project(self):
        # Open a dialog to get project name
        project_name, ok = QInputDialog.getText(self, 'Add Project', 'Enter project name:')
        if ok and project_name:
            self.project_list.addItem(project_name)

    def edit_database_settings(self):
        """
        TODO: add possibility to connect to a shared database (e.g. on shared file location, or e.g. MySQL instance)
        TODO: show database name and location in the dialog
        """
        # Placeholder for editing database settings
        QMessageBox.information(self, "Edit Database Settings", "Database settings would be edited here.")

    def quit_dialog(self, item):
        if can_proceed():
            self.selected_project_name = item.text()
            self.accept()

    def populate_projects(self):
        db_engine = DatabaseEngine().engine
        database_session = sessionmaker(bind=db_engine)
        session = database_session()
        existing_projects = session.query(Project).all()
        list_of_projects = []
        for existing_project in existing_projects:
            list_of_projects.append(existing_project.name)
        session.commit()
        session.close()
        return list_of_projects

    def create_user_layout(self):
        # Layout
        user_layout = QVBoxLayout()
        # Header label
        header_label = QLabel("OpenCAQDA - Select a project")
        header_style = "font-size: 20px; font-weight: bold;"
        header_label.setStyleSheet(header_style)
        user_layout.addWidget(header_label)
        # Description text
        description_label = QLabel(
            "No username found. Please create a user."
        )
        description_label.setWordWrap(True)
        description_label.setMaximumWidth(380)
        description_label.setMinimumHeight(100)
        user_layout.addWidget(description_label)

        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        self.username_field = QLineEdit()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_field)

        password_layout = QHBoxLayout()
        password_label = QLabel("Password:")
        password_field = QLineEdit()
        password_field.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(password_field)

        user_layout.addLayout(username_layout)
        user_layout.addLayout(password_layout)

        # Buttons layout
        #
        user_button = QPushButton("Create User / Login")
        user_button.clicked.connect(self.login_or_create_user)
        user_layout.addWidget(user_button)

        return user_layout

    def login_or_create_user(self):
        # if user exists in DB, check password
        # if user does not exist in DB, show dialog, user does not exist, create one?
        #
        # create user
        username = self.username_field.text()

        db_engine = DatabaseEngine().engine
        database_session = sessionmaker(bind=db_engine)
        session = database_session()
        user_exists = session.scalar(exists(User).where(User.username is username).select())

        if user_exists:
            print("User already exists")
        else:
            dialog = NewUserDialog()
            if dialog.exec():
                new_user = User()
                new_user.username = username
                new_user.password = "whee"
                session.add(new_user)
                session.commit()

                stream = open(CONFIGURATION_FILE_NAME, 'r')
                data = yaml.safe_load(stream)

                data['username'] = username

                with open(CONFIGURATION_FILE_NAME, 'w') as yaml_file:
                    yaml_file.write(yaml.dump(data, default_flow_style=False))

                ConfigurationService().username = username

        session.close()

        self.replace_user_layout()

    def replace_user_layout(self):
        QWidget().setLayout(self.layout())
        layout = self.create_project_list_layout()
        self.setLayout(layout)
