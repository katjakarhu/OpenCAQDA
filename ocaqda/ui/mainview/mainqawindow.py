# This Python file uses the following encoding: utf-8

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QTabWidget, QSplitter, QWidget

from ocaqda.services.projectservice import ProjectService
from ocaqda.ui.mainview.analysistab import AnalysisTab
from ocaqda.ui.mainview.filetab import FileTab
from ocaqda.ui.mainview.infoandnotepanel import InfoAndNotePanel
from ocaqda.ui.mainview.textcontentview import TextContentView
from ocaqda.ui.mainview.textviewer import TextViewer


class MainQAWindow(QMainWindow):

    def __init__(self, name):
        super().__init__()

        self.text_content_panel = None
        self.status_bar = self.statusBar()
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
        center_layout = QHBoxLayout()
        # Left column with tabs
        tab_widget = QTabWidget()
        tab_widget.setMaximumWidth(300)
        analysis_tab = AnalysisTab(self.project_manager)
        files_tab = FileTab(self)
        # Add tabs to tab widget
        tab_widget.addTab(analysis_tab, "Analysis")
        tab_widget.addTab(files_tab, "Files")
        # Middle panel
        self.text_content_panel = TextContentView()
        self.text_content_panel.setMinimumWidth(500)

        # Right panel
        right_panel = InfoAndNotePanel(self.project_manager)
        right_panel.setMaximumWidth(400)
        # Splitter for resizing panels
        splitter = QSplitter()
        splitter.addWidget(tab_widget)
        splitter.addWidget(self.text_content_panel)
        splitter.addWidget(right_panel)
        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(center_layout)
        center_layout.addWidget(splitter)
        self.setCentralWidget(central_widget)

    def set_project(self, name):
        # Each project has its own ProjectManager connected to the MainWindow
        # If project does not exist, it is created
        self.project_manager = ProjectService(name)

        self.setWindowTitle("OpenCAQDA - Project: " + name)

    def add_file_viewer(self, datafile):
        if datafile.file_extension == '.txt':
            text_view = TextViewer()
            text_view.set_text(datafile.file_as_text)
            if not self.is_tab_open(datafile.display_name):
                self.text_content_panel.addTab(text_view, datafile.display_name)
        else:
            pass

    def is_tab_open(self, display_name):
        for i in range(self.text_content_panel.count()):
            if display_name == self.text_content_panel.tabText(i):
                return True
        return False
