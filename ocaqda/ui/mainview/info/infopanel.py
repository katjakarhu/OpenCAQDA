"""
Panel on the right side of the screen displaying where codes have been used
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem


class InfoPanel(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.selected_item = None
        self.main_window = main_window
        layout = QVBoxLayout()
        info_header_label = QLabel("Information:")
        header_style = "font-size: 14px; font-weight: bold;"
        info_header_label.setStyleSheet(header_style)
        layout.addWidget(info_header_label)

        # Description text
        self.info_label = QLabel(
        )
        self.info_label.setWordWrap(True)
        self.info_label.setMaximumWidth(380)
        self.info_label.setMinimumHeight(100)
        self.info_label = QLabel("Info")
        layout.addWidget(self.info_label)

        self.result_list = QTreeWidget()
        self.result_list.setHeaderHidden(True)
        layout.addWidget(self.result_list)

        self.setLayout(layout)

    def set_selected_item_info(self, id, name, type):
        self.result_list.clear()
        self.selected_item = [id, type]
        self.info_label.setText("Selected " + type + " : " + name)
        coded_texts = self.main_window.project_service.get_coded_texts_by_code_id(id)

        for c in coded_texts:
            file = self.main_window.project_service.get_file_by_id(c.data_file_id)
            header_item = QTreeWidgetItem()
            header_item.setText(0, file.display_name)
            child_item = QTreeWidgetItem()
            child_item.setText(0, c.text)
            header_item.addChild(child_item)

            self.result_list.addTopLevelItem(header_item)

        self.result_list.expandAll()
