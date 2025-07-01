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
from ocaqda.ui.mainview.coding.codetab import CodeTab
from ocaqda.ui.mainview.fileselectiontab import FileSelectionTab
from ocaqda.ui.mainview.fileviewer.contenttabview import ContentTabView
from ocaqda.ui.mainview.fileviewer.textandhtmlviewer import TextAndHTMLViewer
from ocaqda.ui.mainview.fileviewer.pdfviewer import PDFViewer
from ocaqda.ui.mainview.infoandnotepanel import InfoAndNotePanel


class MainQAWindow(QMainWindow):

    def __init__(self, name):
        super().__init__()

        self.text_content_panel = ContentTabView()
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
        tab_widget.setMaximumWidth(300)
        code_tab = CodeTab(self.project_service)
        files_tab = FileSelectionTab(self)
        # Add tabs to tab widget
        tab_widget.addTab(code_tab, "Codes")
        tab_widget.addTab(files_tab, "Files")
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

    def add_file_viewer(self, datafile):
        if datafile.file_extension in ('.txt', '.html', '.md'):
            text_view = TextAndHTMLViewer(self, datafile)
            if not self.is_tab_open(datafile.display_name):
                self.text_content_panel.addTab(text_view, datafile.display_name)

            self.text_content_panel.setCurrentIndex(self.get_tab_index(datafile.display_name))


        elif datafile.file_extension == '.pdf':
            pdf_view = PDFViewer(self, datafile)
            if not self.is_tab_open(datafile.display_name):
                self.text_content_panel.addTab(pdf_view, datafile.display_name)

            self.text_content_panel.setCurrentIndex(self.get_tab_index(datafile.display_name))

    def is_tab_open(self, display_name):
        for i in range(self.text_content_panel.count()):
            if display_name == self.text_content_panel.tabText(i):
                return True
        return False

    def get_tab_index(self, display_name):
        for i in range(self.text_content_panel.count()):
            if display_name == self.text_content_panel.tabText(i):
                return int(i)
        return None

    def close_tab(self, display_name):
        for i in range(self.text_content_panel.count()):
            if display_name == self.text_content_panel.tabText(i):
                self.text_content_panel.removeTab(i)

    def get_file_name_from_open_tab(self):
        return self.text_content_panel.tabText(self.text_content_panel.currentIndex())
