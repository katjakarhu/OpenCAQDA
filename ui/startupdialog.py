from PySide6.QtWidgets import QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QPushButton, QInputDialog, \
    QMessageBox, QDialog


class StartUpDialog(QDialog):
    """
    TODO:
    - set OpenCAQDA location on disk for saving database and additional files
    - fix opening of projects
    """

    def __init__(self):
        super().__init__()
        self.selected_project_name = None
        self.setWindowTitle("OpenCAQDA - Select a project")
        self.setGeometry(100, 100, 400, 400)

        # Layout
        layout = QVBoxLayout()

        # Header label
        header_label = QLabel("Welcome to the software!")
        header_style = "font-size: 20px; font-weight: bold;"
        header_label.setStyleSheet(header_style)
        layout.addWidget(header_label)

        # Description text
        description_label = QLabel(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        )
        description_label.setWordWrap(True)
        description_label.setMaximumWidth(380)
        description_label.setMinimumHeight(100)
        layout.addWidget(description_label)

        # List widget for projects
        self.project_list = QListWidget()
        self.project_list.setMinimumHeight(100)
        layout.addWidget(self.project_list)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Add Project Button
        add_button = QPushButton("Add Project")
        add_button.clicked.connect(self.add_project)
        buttons_layout.addWidget(add_button)

        # Edit Database Settings Button, see edit_database_settings method for TODO
        # self.edit_db_button = QPushButton("Edit Database Settings")
        # self.edit_db_button.clicked.connect(self.edit_database_settings)
        # buttons_layout.addWidget(self.edit_db_button)

        layout.addLayout(buttons_layout)

        # Connect project list item click
        self.project_list.itemDoubleClicked.connect(self.quit_dialog)

        self.setLayout(layout)

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
        self.selected_project_name = item.text()
        self.accept()
