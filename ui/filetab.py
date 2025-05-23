from pathlib import Path

from PySide6.QtCore import QDir, QStandardPaths
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView, QPushButton, QFileDialog, QDialog, QListWidget


class FilesTab(QWidget):
    def __init__(self):
        super().__init__()

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
        dialog.setNameFilter("Text files (*.txt *.pdf)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                self.file_list.addItems([str(Path(filename)) for filename in filenames])