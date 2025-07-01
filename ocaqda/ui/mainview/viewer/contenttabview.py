"""
Component holds all the tabs containing opened files
"""
from PySide6.QtWidgets import QTabWidget

from ocaqda.ui.mainview.viewer.pdfviewer import PDFViewer
from ocaqda.ui.mainview.viewer.textandhtmlviewer import TextAndHTMLViewer


class ContentTabView(QTabWidget):
    def __init__(self, main_window, parent=None):
        super().__init__()
        self.main_window = main_window
        self.parent = parent
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(lambda index: self.removeTab(index))

    def add_file_viewer(self, datafile):
        if datafile.file_extension in ('.txt', '.html', '.md'):
            text_view = TextAndHTMLViewer(self, self.main_window, datafile)
            if not self.is_tab_open(datafile.display_name):
                self.addTab(text_view, datafile.display_name)

            self.focus_tab_by_name(datafile.display_name)


        elif datafile.file_extension == '.pdf':
            pdf_view = PDFViewer(self, self.main_window, datafile)
            if not self.is_tab_open(datafile.display_name):
                self.addTab(pdf_view, datafile.display_name)

            self.focus_tab_by_name(datafile.display_name)

    def focus_tab_by_name(self, name):
        self.setCurrentIndex(self.get_tab_index(name))

    def is_tab_open(self, display_name):
        for i in range(self.count()):
            if display_name == self.tabText(i):
                return True
        return False

    def get_tab_index(self, display_name):
        for i in range(self.count()):
            if display_name == self.tabText(i):
                return int(i)
        return None

    def close_tab(self, display_name):
        for i in range(self.count()):
            if display_name == self.tabText(i):
                self.removeTab(i)

    def get_file_name_from_open_tab(self):
        return self.tabText(self.currentIndex())


    def get_open_tab(self):
        return self.currentWidget()
