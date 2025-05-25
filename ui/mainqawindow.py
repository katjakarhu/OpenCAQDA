# This Python file uses the following encoding: utf-8
from PySide6.QtGui import QAction
from PySide6.QtWidgets import *

from data.projectmanager import ProjectManager
from ui.analysistab import AnalysisTab
from ui.filetab import FilesTab
from ui.textcontentview import TextContentView


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
        right_panel = QTextEdit("Right Panel Content")
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
        self.project_manager = ProjectManager(name)

        self.setWindowTitle("OpenCAQDA - Project: " + name)
