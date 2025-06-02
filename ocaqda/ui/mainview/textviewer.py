"""
A component for viewing plain text (txt) files
"""
import re

from PySide6.QtCore import Qt
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat
from PySide6.QtWidgets import QPlainTextEdit

from ocaqda.data.models import CodedText
from ocaqda.services.userservice import UserService

"""
Source: https://stackoverflow.com/questions/57636321/highlighting-portions-of-text-in-qplaintextedit
"""


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent, coded_texts):
        super(SyntaxHighlighter, self).__init__(parent)
        self.coded_text = coded_texts
        self._highlighting_rules = []

        # Strings
        string_format = QTextCharFormat()
        string_format.setBackground(Qt.GlobalColor.yellow)
        string_format.setForeground(Qt.GlobalColor.darkBlue)
        for text in self.coded_text:
            print(text.text)
            self._highlighting_rules.append((re.compile(text.text), string_format))

    def highlightBlock(self, text):
        for pattern, format in self._highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, format)


class TextViewer(QPlainTextEdit):
    def __init__(self, parent, data_file_name, data_file_id):
        super().__init__()
        self.parent = parent
        self.data_file_name = data_file_name
        self.data_file_id = data_file_id
        self.current_selection = ""
        self.setReadOnly(True)
        self.selectionChanged.connect(self.set_current_selection)
        self.setAcceptDrops(True)
        coded_texts = self.parent.project_manager.get_coded_texts(self.data_file_id, self.data_file_name)
        self.highlighter = SyntaxHighlighter(self.document(), coded_texts)

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
                coded_text.file_id = self.data_file_id
                codes = self.parent.project_manager.get_project_codes()
                for code in codes:
                    if code.name == event.mimeData().text():
                        coded_text.code_id = code.code_id
                        break
                coded_text.text = self.current_selection
                coded_text.position = self.textCursor().selectionStart()
                coded_text.created_by = UserService().user.user_id
                coded_text.updated_by = UserService().user.user_id

                print(self.cursor())
                self.parent.project_manager.save_coded_text(coded_text)
        else:
            event.ignore()
            print("Ignore")
