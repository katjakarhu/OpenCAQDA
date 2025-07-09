from PySide6.QtWidgets import QListWidget


class FileList(QListWidget):
    def __init__(self, main_window, parent):
        super().__init__(parent)
        self.main_window = main_window
        self.parent = parent
        self.itemDoubleClicked.connect(self.parent.open_file)

    def mousePressEvent(self, event):
        if self.itemAt(event.pos()) is not None:
            self.main_window.note_tab.set_selected_item_info(self.itemAt(event.pos()).text(), "file")

        super().mousePressEvent(event)

