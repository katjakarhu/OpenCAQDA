from PySide6.QtWidgets import QTabWidget

from ocaqda.data.enums.supportedfiletypes import SupportedFileTypes
from ocaqda.data.models import DataFile
from ocaqda.ui.mainview.textviewer import TextViewer


class TextContentView(QTabWidget):
    def __init__(self, project_manager):
        super().__init__()

    def add_file(self, datafile):
        data = DataFile(datafile)
        if SupportedFileTypes.is_plain_text(datafile.file_type):
            text = data.file_content.decode("utf-8")
            textView = TextViewer()
            textView.set_text(text)
            self.addTab(self, data.name)
