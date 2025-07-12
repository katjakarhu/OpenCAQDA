from PySide6.QtWidgets import QListWidget, QListWidgetItem


class FileList(QListWidget):
    def __init__(self, main_window, parent):
        super().__init__(parent)
        self.main_window = main_window
        self.parent = parent
        self.itemDoubleClicked.connect(self.parent.open_file)

    def mousePressEvent(self, event):
        if self.itemAt(event.pos()) is not None:
            data_file = self.itemAt(event.pos()).data_file
            self.main_window.note_tab.set_selected_item_info(data_file.data_file_id, data_file.display_name, "file")

        super().mousePressEvent(event)


class FileListItem(QListWidgetItem):
    def __init__(self, file):
        super().__init__()

        self.data_file = file
