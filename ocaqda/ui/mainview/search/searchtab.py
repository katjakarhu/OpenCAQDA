import re

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QLineEdit, QPushButton, QHBoxLayout, QTreeWidgetItem

from ocaqda.utils.general_utils import remove_html_tags


class SearchItem(QTreeWidgetItem):
    def __init__(self, parent, search_data):
        super(SearchItem, self).__init__(parent)
        self.location = [search_data[0], search_data[1]]
        self.original_text = search_data[2]

        print(self.location, self.original_text, search_data)
        self.setText(0, "..." + self.original_text.replace('\n', ' ') + "...")


class SearchTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class SearchTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout()

        self.search_list = SearchTree()
        self.search_list.itemDoubleClicked.connect(self.open_file_at_text_location)
        self.search_list.setColumnCount(2)
        self.search_list.setColumnWidth(0, 200)
        self.search_list.setHeaderLabels(['Name', 'Count'])

        self.layout.addWidget(self.search_list)
        self.search_field = QLineEdit()
        self.search_button = QPushButton("Search files")
        self.search_button.clicked.connect(self.search_files)

        self.search_layout = QHBoxLayout()

        self.search_layout.addWidget(self.search_field)
        self.search_layout.addWidget(self.search_button)

        self.layout.addLayout(self.search_layout)

        self.setLayout(self.layout)

        self.search_list.clear()

    def search_files(self):
        search_string = self.search_field.text()

        files = self.main_window.project_service.get_project_files()
        results = dict()
        for f in files:
            if search_string in f.file_as_text:
                plain_text = remove_html_tags(f.file_as_text)
                find_the_word = re.finditer(search_string, plain_text)
                count = 0
                location = []
                for match in find_the_word:
                    count += 1
                    location.append([match.start(), match.end(), plain_text[match.start() - 10:match.end() + 10]])

                print(f.display_name, count)
                results.update({f.display_name: [count, location]})

        self.search_list.clear()

        for k, v in results.items():
            item = QTreeWidgetItem()
            item.setText(0, k)
            item.setText(1, str(v[0]))

            for i in range(len(v[1])):
                child = SearchItem(item, v[1][i])
                child.setExpanded(True)

            self.search_list.addTopLevelItem(item)

    def open_file_at_text_location(self):
        if  self.search_list.currentItem().parent() is None:
            self.open_file()
        else:
            self.search_list.currentItem()

    def open_file(self):
        selected_file = self.search_list.currentItem().text(0)
        for f in self.main_window.project_service.get_project_files():
            if f.display_name == selected_file:
                self.main_window.text_add_file_viewer(f)
