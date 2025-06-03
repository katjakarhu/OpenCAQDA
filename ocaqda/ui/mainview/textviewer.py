"""
A component for viewing plain text (txt) files
"""

from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor
from PySide6.QtWidgets import QPlainTextEdit

from ocaqda.data.models import CodedText
from ocaqda.services.userservice import UserService


class TextViewer(QPlainTextEdit):
    def __init__(self, parent, data_file):
        super().__init__()
        self.highlighter = None
        self.parent = parent
        self.data_file = data_file
        self.setReadOnly(True)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

        self.setPlainText(data_file.file_as_text)
        self.refresh_coded_text_highlight()

    def refresh_coded_text_highlight(self):
        coded_texts = self.parent.project_manager.get_coded_texts(self.data_file.data_file_id,
                                                                  self.data_file.display_name)
        # TODO:
        #  - fetch content as text from data file object, set as text to clear previous formattings
        #  - OR use following:
        # fmt = QTextCharFormat()
        # fmt.setBackground(Qt.GlobalColor.yellow)
        # fmt.setToolTip("code name here")
        # QTextCursor cursor(edit->document());
        # cursor.setPosition(begin, QTextCursor::MoveAnchor);
        # cursor.setPosition(end, QTextCursor::KeepAnchor);
        # cursor.setCharFormat(fmt);
        self.setPlainText(self.data_file.file_as_text)
        cursor = QTextCursor(self.document())
        string_format = QTextCharFormat()
        string_format.setBackground(QColor("yellow"))

        for coded_text in coded_texts:
            cursor.setPosition(coded_text.start_position)
            cursor.setPosition(coded_text.end_position, QTextCursor.MoveMode.KeepAnchor)
            code = self.parent.project_manager.get_code(coded_text.code_id)
            string_format.setToolTip(code.name)
            cursor.mergeCharFormat(string_format)

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            print(e.mimeData().text())
            e.accept()
            current_selection = self.createMimeDataFromSelection().text()
            if current_selection != "":
                coded_text = CodedText()
                coded_text.data_file_id = self.data_file.data_file_id
                codes = self.parent.project_manager.get_project_codes()
                for code in codes:
                    if code.name == e.mimeData().text():
                        coded_text.code_id = code.code_id
                        break
                coded_text.text = current_selection
                coded_text.start_position = self.textCursor().selectionStart()
                coded_text.end_position = self.textCursor().selectionEnd()
                coded_text.created_by = UserService().user.user_id
                coded_text.updated_by = UserService().user.user_id

                self.parent.project_manager.save_coded_text(coded_text)
                self.refresh_coded_text_highlight()
        else:
            e.ignore()
