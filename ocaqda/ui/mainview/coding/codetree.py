from PySide6.QtCore import QMimeData, Qt
from PySide6.QtGui import QBrush, QColor, QDrag
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator

from ocaqda.data.models import CodeRelationship
from ocaqda.utils.colorutils import STANDARD_BACKGROUND_COLOR, HIGHLIGHT_COLOR
from ocaqda.utils.helper_utils import build_tree


class CodeTree(QTreeWidget):
    def __init__(self, project_service, parent):
        super().__init__(parent)
        self.project_service = project_service
        self.parent = parent
        self.setHeaderLabel("Code")

        self.setHeaderHidden(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.populate_code_list()

    def populate_code_list(self):
        self.clear()

        code_relationships = self.project_service.get_parent_child_relationships()

        ids = []
        for cr in code_relationships:
            ids.append(cr.from_code_id)
            ids.append(cr.to_code_id)

        codes = self.project_service.get_project_codes()

        for code in codes:
            if code.code_id not in ids:
                nr = CodeRelationship()
                nr.from_code_id = code.code_id
                code_relationships.append(nr)

        tree = build_tree(code_relationships)


        items = []
        for node in tree:
            code = list(filter(lambda x: x.code_id == node.name, codes))
            item = QTreeWidgetItem([code[0].name])
            for c in node.children:
                if c.name is not None:
                    code = list(filter(lambda x: x.code_id == c.name, codes))
                    child = QTreeWidgetItem()
                    child.setText(0, code[0].name)
                    item.addChild(child)
            items.append(item)

        self.insertTopLevelItems(0, items)

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
            # Add the text as a new item in the tree widget, if one item select, add new item as its child
            item = QTreeWidgetItem([text])
            if len(self.selectedItems()) == 1:
                self.selectedItems()[0].addChild(item)
            else:
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
            if self.currentItem():
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

            relations = dict()
            iterator = QTreeWidgetItemIterator(self)
            while iterator.value():
                itm = iterator.value()
                if itm.parent():
                    relations[itm.parent().text(0)] = itm.text(0)
                iterator += 1

            self.project_service.update_code_relationships(relations)
