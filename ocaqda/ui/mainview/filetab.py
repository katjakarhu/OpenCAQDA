from pathlib import Path

from PySide6.QtCore import QStandardPaths
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget


class FilesTab(QWidget):
    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        self.files_layout = QVBoxLayout()
        # File system model for files tab
        self.file_list = QListWidget(self)
        self.files_layout.addWidget(self.file_list)
        self.files_layout.addWidget(self.file_list)
        # Button to add new text entries
        self.add_files_button = QPushButton("Add files")
        self.add_files_button.clicked.connect(self.add_files)
        self.files_layout.addWidget(self.add_files_button)
        self.setLayout(self.files_layout)

    # Adding files copies them to the project location
    # TODO: design project file system structure
    def add_files(self):
        directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)
        dialog = QFileDialog()
        dialog.setDirectory(directory)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Text and PDF files (*.txt *.pdf)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                self.save_files([str(Path(filename)) for filename in filenames])

    def save_files(self, files):
        self.file_list.addItems(files)
        self.project_manager.save_files(files)
