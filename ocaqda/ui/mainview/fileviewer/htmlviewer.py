"""
A component for viewing plain text files
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor, QUndoCommand, QAction
from PySide6.QtWidgets import QMenu, QTextBrowser

from ocaqda.data.models import CodedText
from ocaqda.services.userservice import UserService
from ocaqda.utils.helper_utils import convert_and_merge_ranges


class HTMLViewer(QTextBrowser, QUndoCommand):
    def __init__(self, parent, data_file):
        super().__init__()
        self.parent = parent
        self.data_file = data_file

        self.codes = self.parent.project_service.get_project_codes()
        self.coded_texts = self.parent.project_service.get_coded_texts(self.data_file.data_file_id,
                                                                       self.data_file.display_name)
        self.highlighter = None

        self.setReadOnly(True)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

        self.setText(data_file.file_as_text)
        self.refresh_coded_text_highlight()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self.textCursor().select(QTextCursor.SelectionType.WordUnderCursor)

        super().mousePressEvent(e)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        menu.addSeparator()

        uncode_submenu = QMenu("Uncode", self)
        for a in uncode_submenu.actions():
            uncode_submenu.removeAction(a)

        c = self.get_used_codes_at_position()
        for code in c:
            code_action = QAction(code, self.remove_code(code))
            uncode_submenu.addAction(code_action)

        menu.addMenu(uncode_submenu)

        menu.exec(event.globalPos())

    def get_used_codes_at_position(self):
        cursor = self.textCursor()
        used_codes = set()

        self.coded_texts = self.parent.project_service.get_coded_texts(self.data_file.data_file_id,
                                                                       self.data_file.display_name)
        for coded_text in self.coded_texts:
            if coded_text.start_position <= cursor.position() <= coded_text.end_position:
                code = next(filter(lambda x: x.code_id == coded_text.code_id, self.codes), None)
                used_codes.add(code.name)

        return used_codes

    def remove_code(self, code):
        cursor = self.textCursor()
        if cursor.hasSelection():
            for coded_text in self.coded_texts:
                if coded_text.text == cursor.selectedText():
                    print("remove code")
        else:
            for coded_text in self.coded_texts:
                if coded_text.start_position <= cursor.position() <= coded_text.end_position:
                    print("remove codes that match the cursor position")

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
            current_selection = self.createMimeDataFromSelection().text()
            if current_selection != "":
                self.add_code_to_selected_text(current_selection, e)
        else:
            e.ignore()

    def add_code_to_selected_text(self, current_selection, e):
        coded_text = CodedText()
        coded_text.data_file_id = self.data_file.data_file_id
        self.codes = self.parent.project_service.get_project_codes()
        for code in self.codes:
            if code.name == e.mimeData().text():
                coded_text.code_id = code.code_id
                break
        coded_text.text = current_selection
        coded_text.start_position = self.textCursor().selectionStart()
        coded_text.end_position = self.textCursor().selectionEnd()
        coded_text.created_by = UserService().user.user_id
        coded_text.updated_by = UserService().user.user_id
        self.parent.project_service.save_coded_text(coded_text)
        self.refresh_coded_text_highlight()

    def refresh_coded_text_highlight(self):
        self.coded_texts = self.parent.project_service.get_coded_texts(self.data_file.data_file_id,
                                                                       self.data_file.display_name)
        # Ugly solution? Resets all formatting by reloading text and reapplying formatting
        self.setText(self.data_file.file_as_text)
        cursor = QTextCursor(self.document())
        string_format = QTextCharFormat()
        string_format.setBackground(QColor("yellow"))

        positions = []

        for coded_text in self.coded_texts:
            code = next(filter(lambda x: x.code_id == coded_text.code_id, self.codes), None)
            positions.append([coded_text.start_position, coded_text.end_position, code.name])

        merged_positions = convert_and_merge_ranges(positions)

        for item in merged_positions:
            cursor.setPosition(item[0])
            cursor.setPosition(item[1], QTextCursor.MoveMode.KeepAnchor)
            string_format.setToolTip(str(item[2]))
            cursor.mergeCharFormat(string_format)
