"""
Component holds all the tabs containing opened files
"""
from PySide6.QtWidgets import QTabWidget


class ContentTabView(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(lambda index: self.removeTab(index))
