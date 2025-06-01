from PySide6.QtWidgets import QTabWidget

from ocaqda.ui.mainview.textviewer import TextViewer


class TextContentView(QTabWidget):
    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        # self.addTab(self, "hello")

    def add_file(self, datafile):
        if datafile.file_extension == '.txt':
            text_view = TextViewer()
            text_view.set_text(datafile.file_as_text)
            self.addTab(text_view, datafile.display_name)
