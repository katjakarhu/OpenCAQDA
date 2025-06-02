"""
A dialog for creating a new user if one is not specified in opencaqda-settings.yaml

"""

from PySide6.QtWidgets import QVBoxLayout, QLabel, QDialog, QPushButton, QMessageBox


class NewUserDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create New User")
        self.setGeometry(100, 100, 300, 100)

        layout = QVBoxLayout()

        self.label = QLabel("Do you want to create a new user?")
        layout.addWidget(self.label)

        self.yes_button = QPushButton("Yes")
        self.yes_button.clicked.connect(self.on_yes_click)
        layout.addWidget(self.yes_button)

        self.no_button = QPushButton("No")
        self.no_button.clicked.connect(self.on_no_click)
        layout.addWidget(self.no_button)

        self.setLayout(layout)

    def on_yes_click(self):
        QMessageBox.information(self, "Decision", "You chose to create a new user.")
        self.accept()

    def on_no_click(self):
        QMessageBox.information(self, "Decision", "You chose not to create a new user.")
        self.reject()
