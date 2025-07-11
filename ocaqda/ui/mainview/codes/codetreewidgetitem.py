from PySide6.QtWidgets import QTreeWidgetItem


class CodeTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, code):
        QTreeWidgetItem.__init__(self, parent)
        self.code = code
