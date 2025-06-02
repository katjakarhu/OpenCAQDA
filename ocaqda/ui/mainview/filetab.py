"""
A tab that displays the files on the left side of the screen
"""
from pathlib import Path

from PySide6.QtCore import QStandardPaths
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget


class FileTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.listed_files = None
        self.files_layout = QVBoxLayout()
        # File system model for files tab
        self.file_list = QListWidget(self)
        self.file_list.itemDoubleClicked.connect(self.open_file)
        self.populate_file_list()
        self.files_layout.addWidget(self.file_list)
        # Button to add new text entries
        self.add_files_button = QPushButton("Add files")
        self.add_files_button.clicked.connect(self.add_files)
        self.files_layout.addWidget(self.add_files_button)
        # Button to add new text entries
        self.manage_files_button = QPushButton("Manage files")
        self.manage_files_button.clicked.connect(self.manage_files())
        self.files_layout.addWidget(self.manage_files_button)
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
                self.populate_file_list()

    def get_added_files(self):
        return [x.display_name for x in self.listed_files]

    def save_files(self, files):
        print(files)
        items = self.get_added_files()
        print(items)

        filenames = [f for f in files if f[f.rfind('/') + 1:]
                     not in items]
        print(filenames)
        self.file_list.addItems(filenames)

        return self.main_window.project_manager.save_files(filenames)

    def populate_file_list(self):
        self.file_list.clear()
        self.listed_files = self.main_window.project_manager.get_project_files()
        for f in self.listed_files:
            self.file_list.addItem(f.display_name)

    def open_file(self):
        selected_file = self.file_list.currentItem().text()
        print(selected_file)
        for f in self.listed_files:
            if f.display_name == selected_file:
                if f.file_extension == '.pdf':
                    print("pdf")
                elif f.file_extension == '.txt':
                    print("txt")
                    self.main_window.add_file_viewer(f)

    def manage_files(self):
        # TODO open new view for deleting and renaming files
        pass
