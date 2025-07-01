"""
The full screen view that contains all the UI elements in three columns.
Left: codes and files
Center: file contents
Right: info and notes

"""
# This Python file uses the following encoding: utf-8

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QTabWidget, QSplitter, QWidget

from ocaqda.services.projectservice import ProjectService
from ocaqda.ui.mainview.codes.codetab import CodeTab
from ocaqda.ui.mainview.files.fileselectiontab import FileSelectionTab
from ocaqda.ui.mainview.infoandnotepanel import InfoAndNotePanel
from ocaqda.ui.mainview.search.searchtab import SearchTab
from ocaqda.ui.mainview.viewer.contenttabview import ContentTabView


class MainQAWindow(QMainWindow):

    def __init__(self, name):
        super().__init__()

        self.text_content_panel = ContentTabView(self)
        self.status_bar = self.statusBar()
        self.project_service = None
        self.set_project(name)
        self.initialize_layout()

    def initialize_layout(self):
        self.setGeometry(100, 100, 800, 600)
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        tools_menu = menu_bar.addMenu('&Tools')
        # save menu item
        save_action = QAction('&Save project', self)
        save_action.setStatusTip('Save project')
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.project_service.save_project)
        file_menu.addAction(save_action)
        file_menu.addSeparator()

        visualize_action = QAction('&Visualize project', self)
        # tools_menu.addAction(visualize_action)

        # Main layout
        center_layout = QHBoxLayout()
        # Left column with tabs
        tab_widget = QTabWidget()
        tab_widget.setMaximumWidth(500)
        code_tab = CodeTab(self.project_service)
        files_tab = FileSelectionTab(self)
        search_tab = SearchTab(self)
        # Add tabs to tab widget
        tab_widget.addTab(code_tab, "Codes")
        tab_widget.addTab(files_tab, "Files")
        tab_widget.addTab(search_tab, "Search")
        # Middle panel
        self.text_content_panel.setMinimumWidth(500)

        # Right panel
        right_panel = InfoAndNotePanel(self.project_service)
        right_panel.setMaximumWidth(400)
        # Splitter for resizing panels
        splitter = QSplitter()
        splitter.addWidget(tab_widget)
        splitter.addWidget(self.text_content_panel)
        # splitter.addWidget(right_panel)
        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(center_layout)
        center_layout.addWidget(splitter)
        self.setCentralWidget(central_widget)

    def set_project(self, name):
        # Each project has its own ProjectManager connected to the MainWindow
        # If project does not exist, it is created
        self.project_service = ProjectService(name)

        self.setWindowTitle("OpenCAQDA - Project: " + name)
