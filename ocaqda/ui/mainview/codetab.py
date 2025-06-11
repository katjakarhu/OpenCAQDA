"""
A tab on left side of the screen that displays the codes

Right mouse button: Codes can be arranged to a hierarchy by drag and drop

Left mouse button: Coding is done by dragging the code over a selected text in the center text component

"""
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QBrush, QColor, QDrag
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QPushButton, QTreeWidgetItem, QLineEdit, \
    QTreeWidgetItemIterator, QHBoxLayout

from ocaqda.utils.colorutils import STANDARD_BACKGROUND_COLOR, HIGHLIGHT_COLOR


# TODO:
# manage codes button and view
# drag and drop coding for PDF

class CodeTree(QTreeWidget):
    def __init__(self, project_service, parent):
        super().__init__(parent)
        self.project_service = project_service
        self.parent = parent
        self.setHeaderLabel("Codes")

        self.setHeaderHidden(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.populate_code_list()

    def populate_code_list(self):
        self.clear()
        for code in self.project_service.get_project_codes():
            self.add_item_to_tree(code.name)

    def add_and_save_code(self):
        # Open a dialog to get text input
        text = self.parent.add_code_field.text()
        if text:
            # Limit the text length to 512 characters
            if len(text) > 0 and len(self.findItems(text, Qt.MatchFlag.MatchExactly)) == 0:
                self.project_service.save_code(text)
                self.populate_code_list()

    def add_item_to_tree(self, text):
        if len(text) > 0 and len(self.findItems(text, Qt.MatchFlag.MatchExactly)) == 0:
            # Add the text as a new item in the tree widget
            item = QTreeWidgetItem([text])
            self.addTopLevelItem(item)

    def filter_codes(self):
        filter_text = self.parent.filter_field.text().lower()
        if filter_text == "":
            iterator = QTreeWidgetItemIterator(self)
            while iterator.value():
                item = iterator.value()
                item.setBackground(0, QBrush(QColor(STANDARD_BACKGROUND_COLOR)))
                item.setHidden(False)
                iterator += 1
        else:
            iterator = QTreeWidgetItemIterator(self)
            while iterator.value():
                item = iterator.value()

                item_text = item.text(0).lower()
                if filter_text not in item_text:
                    item.setHidden(True)
                    item.setBackground(0, QBrush(QColor(STANDARD_BACKGROUND_COLOR)))
                else:
                    item.setHidden(False)
                    item.setBackground(0, QBrush(QColor(HIGHLIGHT_COLOR)))
                    while item.parent():
                        item.parent().setExpanded(True)
                        parent_text = item.parent().text(0).lower()
                        item.parent().setHidden(filter_text not in parent_text)
                        if filter_text not in parent_text:
                            item.parent().setBackground(0, QBrush(QColor(
                                STANDARD_BACKGROUND_COLOR)))
                        else:
                            item.parent().setBackground(0, QBrush(QColor(HIGHLIGHT_COLOR)))

                        item = item.parent()
                iterator += 1

    def mousePressEvent(self, event):
        self.setCurrentItem(self.itemAt(event.pos()))

        if event.button() == Qt.MouseButton.LeftButton:
            mime_data = QMimeData()
            mime_data.setText(self.currentItem().text(0))

            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.CopyAction)
        else:
            super().mousePressEvent(event)

    def dropEvent(self, event):
        if event.source() == self:
            super().dropEvent(event)


class CodeTab(QWidget):
    def __init__(self, project_service):
        super().__init__()

        self.project_service = project_service
        analysis_layout = QVBoxLayout()
        # Tree widget for analysis tab
        self.code_tree = CodeTree(project_service, self)
        self.filter_field = QLineEdit()
        self.filter_field.setPlaceholderText("Filter codes...")

        self.filter_field.textChanged.connect(self.code_tree.filter_codes)
        analysis_layout.addWidget(self.filter_field)

        analysis_layout.addWidget(self.code_tree)

        # Button to add new text entries
        add_code_layout = QHBoxLayout()
        self.add_code_field = QLineEdit()
        self.add_button = QPushButton("Add code")
        self.add_button.clicked.connect(self.code_tree.add_and_save_code)
        add_code_layout.addWidget(self.add_code_field)
        add_code_layout.addWidget(self.add_button)
        analysis_layout.addLayout(add_code_layout)

        self.manage_codes_button = QPushButton("Manage codes")
        self.manage_codes_button.clicked.connect(self.manage_codes)
        analysis_layout.addWidget(self.manage_codes_button)
        self.setLayout(analysis_layout)

    def manage_codes(self):
        raise "Implement me!"
