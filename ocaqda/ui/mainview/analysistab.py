from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QPushButton, QTreeWidgetItem, QLineEdit, \
    QTreeWidgetItemIterator, QHBoxLayout

from ocaqda.utils.colorutils import STANDARD_BACKGROUND_COLOR, HIGHLIGHT_COLOR


# TODO:
# add quick filter for codes
# manage codes button and view
# drag and drop coding

class AnalysisTab(QWidget, ):
    def __init__(self, project_manager, /):
        super().__init__()
        self.project_manager = project_manager
        analysis_layout = QVBoxLayout()
        # Tree widget for analysis tab
        self.filter_field = QLineEdit()
        self.filter_field.setPlaceholderText("Filter codes...")

        self.filter_field.textChanged.connect(self.filter_codes)
        analysis_layout.addWidget(self.filter_field)

        self.analysis_tree = QTreeWidget()
        self.analysis_tree.setHeaderLabel("Codes")
        self.analysis_tree.setHeaderHidden(True)
        # TODO: move this d&d functionality to new view managecdes.py
        self.analysis_tree.setDragDropMode(QTreeWidget.InternalMove)
        self.analysis_tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.analysis_tree.setDragEnabled(True)
        self.analysis_tree.setAcceptDrops(True)
        self.analysis_tree.setDropIndicatorShown(True)
        analysis_layout.addWidget(self.analysis_tree)

        # Button to add new text entries
        add_code_layout = QHBoxLayout()
        self.add_code_field = QLineEdit()
        self.add_button = QPushButton("Add codes")
        self.add_button.clicked.connect(self.add_tree_entry)
        add_code_layout.addWidget(self.add_code_field)
        add_code_layout.addWidget(self.add_button)
        analysis_layout.addLayout(add_code_layout)
        self.setLayout(analysis_layout)

    def add_tree_entry(self):
        # Open a dialog to get text input
        text = self.add_code_field.text()
        if text:
            # Limit the text length to 512 characters
            text = text[:512]

            if len(text) > 0 and len(self.analysis_tree.findItems(text, Qt.MatchFlag.MatchExactly)) == 0:
                # Add the text as a new item in the tree widget
                item = QTreeWidgetItem([text])
                self.analysis_tree.addTopLevelItem(item)
                self.project_manager.save_code(text)

    def filter_codes(self):
        filter_text = self.filter_field.text().lower()
        if filter_text == "":
            iterator = QTreeWidgetItemIterator(self.analysis_tree)
            while iterator.value():
                item = iterator.value()
                item.setBackground(0, QBrush(QColor(STANDARD_BACKGROUND_COLOR)))
                item.setHidden(False)
                iterator += 1
        else:
            iterator = QTreeWidgetItemIterator(self.analysis_tree)
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
                        if (filter_text not in parent_text):
                            item.parent().setBackground(0, QBrush(QColor(
                                STANDARD_BACKGROUND_COLOR)))
                        else:
                            item.parent().setBackground(0, QBrush(QColor(HIGHLIGHT_COLOR)))

                        item = item.parent()
                iterator += 1
