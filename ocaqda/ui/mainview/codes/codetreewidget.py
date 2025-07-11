from PySide6.QtCore import QMimeData, Qt
from PySide6.QtGui import QBrush, QColor, QDrag
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator

from ocaqda.ui.mainview.codes.codetreewidgetitem import CodeTreeWidgetItem
from ocaqda.utils.coding_utils import create_tree
from ocaqda.utils.colorutils import STANDARD_BACKGROUND_COLOR, HIGHLIGHT_COLOR


class CodeTreeWidget(QTreeWidget):
    def __init__(self, main_window, parent):
        super().__init__(parent)
        self.coded_texts = None
        self.main_window = main_window
        self.parent = parent
        self.setColumnCount(2)
        self.setHeaderLabels(["Code", "Usages"])

        self.setHeaderHidden(False)
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.populate_code_list()

    def update_code_counts(self):
        self.coded_texts = self.main_window.project_service.get_coded_texts_for_current_project()
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            count = len([x.coded_text_id for x in self.coded_texts if x.code_id == item.code.code_id])
            item.setText(1, str(count))

            self.update_child_code_count(item)

    def update_child_code_count(self, item):
        for j in range(item.childCount()):
            count = len([x.coded_text_id for x in self.coded_texts if x.code_id == item.child(j).code.code_id])
            item.child(j).setText(1, str(count))
            if item.child(j).childCount() > 0:
                self.update_child_code_count(item.child(j))

    def populate_code_list(self):
        self.clear()

        code_relationships = self.main_window.project_service.get_parent_child_relationships()
        codes = self.main_window.project_service.get_project_codes()
        self.coded_texts = self.main_window.project_service.get_coded_texts_for_current_project()

        tree = create_tree(code_relationships, codes)

        items = []
        for node in tree:
            item = CodeTreeWidgetItem(self, node.code)
            item.setText(0, node.code.name)
            count = len([x.coded_text_id for x in self.coded_texts if x.code_id == node.code.code_id])
            item.setText(1, str(count))
            if node.children is not None:
                self.add_children_to_parent(item, node)
            items.append(item)

        self.insertTopLevelItems(0, items)

    def add_children_to_parent(self, item, node):
        for c in node.children:
            if c.code.name is not None:
                count = len([x.coded_text_id for x in self.coded_texts if x.code_id == c.code.code_id])
                child = CodeTreeWidgetItem(item, c.code)
                child.setText(0, c.code.name)
                child.setText(1, str(count))
                item.addChild(child)
                if c.children is not None:
                    self.add_children_to_parent(child, c)

    def add_and_save_code(self, text):
        if text:
            # Limit the text length to 512 characters
            if len(text) > 0 and len(self.findItems(text, Qt.MatchFlag.MatchExactly)) == 0:
                self.main_window.project_service.save_code(text)
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

        if self.itemAt(event.pos()) is not None:
            self.main_window.note_tab.set_selected_item_info(self.itemAt(event.pos()).text(0), "code")

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
                    if itm.parent().code in relations.keys():
                        relations[itm.parent().code].append(itm.code)
                    else:
                        relations[itm.parent().code] = [itm.code]
                iterator += 1

            self.main_window.project_service.update_code_parent_child_relationships(relations)

    def mouseDoubleClickEvent(self, event, /):
        if self.itemAt(event.pos()) is not None:
            self.main_window.info_tab.set_selected_item_info(self.itemAt(event.pos()).text(0), "code")
