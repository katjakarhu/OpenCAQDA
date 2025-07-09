"""
A component for viewing text or HTML content
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor, QUndoCommand, QColorConstants
from PySide6.QtWidgets import QMenu, QTextBrowser, QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QPushButton

from ocaqda.data.models import CodedText
from ocaqda.services.userservice import UserService
from ocaqda.ui.mainview.codes.addcodedialog import AddCodeDialog
from ocaqda.utils.coding_utils import convert_and_merge_ranges


class TextAndHTMLViewer(QWidget):
    def __init__(self, parent, main_window, datafile):
        super(TextAndHTMLViewer, self).__init__(parent)
        self.parent = parent
        self.datafile = datafile
        self.main_window = main_window
        self.viewer = HTMLViewer(self.parent, self.main_window, self.datafile)
        self.search_field = QLineEdit()
        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search_text)
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()

        search_layout.addWidget(self.search_field)
        search_layout.addWidget(self.search_button)

        layout.addWidget(self.viewer)
        layout.addLayout(search_layout)
        self.setLayout(layout)

    def search_text(self):
        text = self.search_field.text()
        self.viewer.find(text)


class HTMLViewer(QTextBrowser, QUndoCommand):
    def __init__(self, parent, main_window, data_file):
        super().__init__()
        self.parent = parent
        self.main_window = main_window
        self.data_file = data_file

        self.codes = self.main_window.project_service.get_project_codes()
        self.coded_texts = self.main_window.project_service.get_coded_texts_by_file(self.data_file.data_file_id,
                                                                                    self.data_file.display_name)
        self.update_text()

        self.highlighter = None

        self.setReadOnly(True)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

        self.setOpenExternalLinks(False)
        # self.setOpenLinks(False)

        self.refresh_coded_text_highlight()

    def update_text(self):
        if self.data_file.file_extension == '.md':
            self.setMarkdown(self.data_file.file_as_text)
        elif self.data_file.file_extension == '.html':
            self.setHtml(self.data_file.file_as_text)
        else:
            self.setText(self.data_file.file_as_text)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self.textCursor().select(QTextCursor.SelectionType.WordUnderCursor)

        super().mousePressEvent(e)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        menu.addSeparator()

        new_code_action = menu.addAction("New code")
        new_code_action.triggered.connect(lambda: self.add_new_code())
        menu.addSeparator()

        invivo_code_action = menu.addAction("Code in-vivo")
        invivo_code_action.triggered.connect(lambda: self.code_in_vivo())
        menu.addSeparator()

        uncode_submenu = QMenu("Uncode", self)
        for a in uncode_submenu.actions():
            uncode_submenu.removeAction(a)

        c = self.get_used_codes_at_position()
        for code in c:
            action = uncode_submenu.addAction(code)
            action.triggered.connect(lambda: self.remove_code(code))
        menu.addMenu(uncode_submenu)

        menu.exec(event.globalPos())

    def get_used_codes_at_position(self):
        cursor = self.textCursor()
        used_codes = set()

        self.coded_texts = self.main_window.project_service.get_coded_texts_by_file(self.data_file.data_file_id,
                                                                                    self.data_file.display_name)
        for coded_text in self.coded_texts:
            if coded_text.start_position <= cursor.position() <= coded_text.end_position:
                code = next(filter(lambda x: x.code_id == coded_text.code_id, self.codes), None)
                used_codes.add(code.name)

        return used_codes

    def remove_code(self, code_name):
        cursor = self.textCursor()

        for coded_text in self.coded_texts:
            if coded_text.start_position <= cursor.position() <= coded_text.end_position:
                code = self.main_window.project_service.get_code_from_coded_text(coded_text)
                if code is not None and code.name == code_name:
                    self.remove_highlight(coded_text)
                    self.coded_texts.remove(coded_text)
                    self.main_window.project_service.delete_coded_text(coded_text)
                    self.refresh_coded_text_highlight()

        self.main_window.code_tab.code_tree.populate_code_list()

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
            name = e.mimeData().text()
            self.code_selection(name)
        else:
            e.ignore()

    def code_selection(self, name):
        current_selection = self.createMimeDataFromSelection().text()
        if current_selection != "":
            self.add_code_to_selected_text(current_selection, name)
            self.main_window.code_tab.code_tree.populate_code_list()

    def add_code_to_selected_text(self, current_selection, name):
        coded_text = CodedText()
        coded_text.data_file_id = self.data_file.data_file_id
        self.codes = self.main_window.project_service.get_project_codes()
        for code in self.codes:
            if code.name == name:
                coded_text.code_id = code.code_id
                break
        coded_text.text = current_selection
        coded_text.start_position = self.textCursor().selectionStart()
        coded_text.end_position = self.textCursor().selectionEnd()
        coded_text.created_by = UserService().user.user_id
        coded_text.updated_by = UserService().user.user_id
        coded_text.project_id = self.main_window.project_service.current_project.project_id
        self.main_window.project_service.save_coded_text(coded_text)
        self.refresh_coded_text_highlight()

    def refresh_coded_text_highlight(self):

        self.coded_texts = self.main_window.project_service.get_coded_texts_by_file(self.data_file.data_file_id,
                                                                                    self.data_file.display_name)
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

    def remove_highlight(self, coded_text):
        cursor = QTextCursor(self.document())
        string_format = QTextCharFormat()
        string_format.setBackground(QColorConstants.Transparent)
        cursor.setPosition(coded_text.start_position)
        cursor.setPosition(coded_text.end_position, QTextCursor.MoveMode.KeepAnchor)
        string_format.setToolTip("")
        cursor.mergeCharFormat(string_format)

    def add_new_code(self):
        dialog = AddCodeDialog(self.main_window, self)
        dialog.exec()

    def code_in_vivo(self):
        text = self.createMimeDataFromSelection().text()
        self.main_window.code_tab.code_tree.add_and_save_code(text)
        self.code_selection(text)
