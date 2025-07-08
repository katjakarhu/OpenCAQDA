import re

from PySide6.QtGui import QColor, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QLineEdit, QPushButton, QHBoxLayout, QTreeWidgetItem

from ocaqda.utils.general_utils import remove_html_tags


class SearchItem(QTreeWidgetItem):
    def __init__(self, parent, id_number, search_data):
        super(SearchItem, self).__init__(parent)
        self.id_number = id_number
        self.surrounding_text = search_data[2]
        self.searched_text = search_data[3]

        self.setText(0, "..." + self.surrounding_text.replace('\n', ' ') + "...")


class SearchTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class SearchTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.files = None
        self.main_window = main_window
        self.layout = QVBoxLayout()

        self.search_list = SearchTree()
        self.search_list.itemDoubleClicked.connect(self.open_file_at_text_location)
        self.search_list.setColumnCount(2)
        self.search_list.setColumnWidth(0, 400)
        self.search_list.setHeaderLabels(['Name', 'Count'])

        self.layout.addWidget(self.search_list)
        self.search_field = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_files)
        # TODO: add search options for notes, files, codes

        self.search_layout = QHBoxLayout()

        self.search_layout.addWidget(self.search_field)
        self.search_layout.addWidget(self.search_button)

        self.layout.addLayout(self.search_layout)

        self.setLayout(self.layout)

        self.search_list.clear()

    def search_files(self):
        search_string = self.search_field.text()

        if search_string == "":
            self.search_list.clear()
            return

        self.files = self.main_window.project_service.get_project_files()
        results = dict()
        for f in self.files:
            if search_string in f.file_as_text:
                plain_text = remove_html_tags(f.file_as_text)
                found_search_items = re.finditer(search_string, plain_text)
                count = 0
                location = []
                for match in found_search_items:
                    count += 1
                    location.append(
                        [match.start(), match.end(), plain_text[match.start() - 10:match.end() + 30], match.group()])

                results.update({f.display_name: [count, location]})

        self.search_list.clear()

        for k, v in results.items():
            item = QTreeWidgetItem()
            item.setText(0, k)
            item.setText(1, str(v[0]))

            for i in range(len(v[1])):
                child = SearchItem(item, i, v[1][i])
                child.setExpanded(True)

            self.search_list.addTopLevelItem(item)

    def open_file_at_text_location(self):
        if self.search_list.currentItem().parent() is None:
            selected_file = self.search_list.currentItem().text(0)
            self.open_file(selected_file)
        else:
            selected_file = self.search_list.currentItem().parent().text(0)
            search_result = self.search_list.currentItem()
            self.open_file(selected_file)
            self.scroll_to_found_item(search_result, selected_file)

    def scroll_to_found_item(self, search_result, selected_file):
        tab = self.main_window.text_content_panel.get_open_tab()
        text = ""
        if selected_file.endswith('.pdf'):
            text = tab.text_content.viewer.toPlainText()

            location = self.find_locations_in_text(search_result, text)
            cursor = tab.text_content.viewer.textCursor()
            self.set_cursor_to_found_text_with_highlight(cursor, location, search_result)
            tab.text_content.viewer.setTextCursor(cursor)

        else:
            text = tab.viewer.toPlainText()
            location = self.find_locations_in_text(search_result, text)

            cursor = tab.viewer.textCursor()
            self.set_cursor_to_found_text_with_highlight(cursor, location, search_result)
            tab.viewer.setTextCursor(cursor)

    def find_locations_in_text(self, search_result, text):
        found_search_items = re.finditer(search_result.searched_text, text)
        location = list()
        for match in found_search_items:
            location.append(
                [match.start(), match.end()])
        return location

    def set_cursor_to_found_text_with_highlight(self, cursor, location, search_result):
        string_format = QTextCharFormat()
        string_format.setBackground(QColor("pink"))
        if len(location) > 0:
            cursor.setPosition(location[search_result.id_number][0])
            cursor.setPosition(location[search_result.id_number][1],
                               QTextCursor.MoveMode.KeepAnchor)
            cursor.mergeCharFormat(string_format)

    def open_file(self, selected_file):
        for f in self.main_window.project_service.get_project_files():
            if f.display_name == selected_file:
                self.main_window.text_content_panel.add_file_viewer(f)
