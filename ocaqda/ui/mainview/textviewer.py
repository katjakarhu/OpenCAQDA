"""
A component for viewing plain text (txt) files
"""

from PySide6.QtWidgets import QPlainTextEdit


class TextViewer(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def set_text(self, text):
        self.setPlainText(text)
