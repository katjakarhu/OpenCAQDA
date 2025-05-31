# This Python file uses the following encoding: utf-8
from PySide6.QtGui import QAction
from PySide6.QtWidgets import *

from src.services.projectservice import ProjectService
from src.ui.mainview.analysistab import AnalysisTab
from src.ui.mainview.filetab import FilesTab
from src.ui.mainview.textcontentview import TextContentView


class InfoAndNotePanel(QWidget):
    def __init__(self, project_manager):
        super().__init__()
        layout = QVBoxLayout()
        info_header_label = QLabel("Information:")
        header_style = "font-size: 14px; font-weight: bold;"
        info_header_label.setStyleSheet(header_style)
        layout.addWidget(info_header_label)

        # Description text
        info_label = QLabel(
            "Info here"
        )
        info_label.setWordWrap(True)
        info_label.setMaximumWidth(380)
        info_label.setMinimumHeight(100)
        self.info_label = QLabel("Info")
        self.note_area = QTextEdit("jdksjdksak")
        layout.addWidget(self.info_label)

        note_header_label = QLabel("Notes:")
        note_header_label.setStyleSheet(header_style)

        note_instruction_label = QLabel(
            "Please select a file or a code to attach notes to. You can view and export notes from the tools menu")
        note_instruction_label.setWordWrap(True)

        layout.addWidget(note_header_label)
        layout.addWidget(note_instruction_label)
        layout.addWidget(self.note_area)
        self.setLayout(layout)


class MainQAWindow(QMainWindow):

    def __init__(self, name, /):
        super().__init__()

        self.project_manager = None
        self.set_project(name)
        self.initialize_layout()

    def initialize_layout(self):
        self.setGeometry(100, 100, 800, 600)
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        edit_menu = menu_bar.addMenu('&Edit')
        help_menu = menu_bar.addMenu('&Help')
        # save menu item
        save_action = QAction('&Save project', self)
        save_action.setStatusTip('Save project')
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.project_manager.save_project)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        # Main layout
        main_layout = QHBoxLayout()
        # Left column with tabs
        tab_widget = QTabWidget()
        tab_widget.setMaximumWidth(500)
        analysis_tab = AnalysisTab(self.project_manager)
        files_tab = FilesTab(self.project_manager)
        # Add tabs to tab widget
        tab_widget.addTab(analysis_tab, "Analysis")
        tab_widget.addTab(files_tab, "Files")
        # Middle panel
        middle_panel = TextContentView(self.project_manager)
        # Right panel
        right_panel = InfoAndNotePanel(self.project_manager)
        # Splitter for resizing panels
        splitter = QSplitter()
        splitter.addWidget(tab_widget)
        splitter.addWidget(middle_panel)
        splitter.addWidget(right_panel)
        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        main_layout.addWidget(splitter)
        self.setCentralWidget(central_widget)

    def set_project(self, name):
        # Each project has it's own ProjectManager connected to the MainWindow
        # If project does not exist, it is created
        self.project_manager = ProjectService(name)

        self.setWindowTitle("OpenCAQDA - Project: " + name)
