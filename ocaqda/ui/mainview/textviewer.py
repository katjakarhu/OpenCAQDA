"""
A component for viewing plain text (txt) files
"""

from PySide6.QtWidgets import QPlainTextEdit

from ocaqda.data.models import CodedText
from ocaqda.services.userservice import UserService


class TextViewer(QPlainTextEdit):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.current_selection = ""
        self.setReadOnly(True)
        self.selectionChanged.connect(self.set_current_selection)
        self.setAcceptDrops(True)

    def set_text(self, text):
        self.setPlainText(text)

    def set_current_selection(self):
        self.current_selection = self.createMimeDataFromSelection().text()

    def dropEvent(self, event):
        print("bar")

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
            print(event.mimeData().text())
            if self.current_selection != "":
                coded_text = CodedText()
                coded_text.text = self.current_selection
                # coded_text.code_id =
                # coded_text.data_file_id
                coded_text.created_by = UserService().user.user_id
                coded_text.updated_by = UserService().user.user_id
                self.parent.project_manager.save_coded_text(coded_text)
        else:
            event.ignore()
            print("Ignore")
