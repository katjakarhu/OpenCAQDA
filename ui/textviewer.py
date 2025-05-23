from PySide6.QtGui import QAbstractTextDocumentLayout, QTextDocument
from PySide6.QtWidgets import QWidget, QPlainTextEdit


class TextViewer(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)



    def set_text(self, text):
        self.setPlainText(text)