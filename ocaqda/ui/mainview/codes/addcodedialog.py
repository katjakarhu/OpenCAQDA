from PySide6.QtWidgets import QDialog, QPushButton, QHBoxLayout, QComboBox


class AddCodeDialog(QDialog):
    def __init__(self, main_window, parent=None):
        super().__init__()
        self.main_window = main_window
        self.parent = parent

        self.setWindowTitle("Add Code")
        self.setGeometry(100, 100, 400, 100)

        # Create QLineEdit
        self.line_edit = QComboBox(self)
        self.line_edit.setEditable(True)
        self.line_edit.setInsertPolicy(QComboBox.InsertPolicy.InsertAtTop)

        for item in self.main_window.project_service.get_project_codes():
            self.line_edit.addItem(item.name, item)

        # Create QPushButton
        self.button = QPushButton("Add", self)
        self.button.clicked.connect(self.on_button_click)

        # Create layout and add widgets
        layout = QHBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)

        # Set dialog layout
        self.setLayout(layout)

    def on_button_click(self):
        text = self.line_edit.currentText()
        if len(text) > 255:
            text = text[:255]

        self.main_window.code_tab.code_tree.add_and_save_code(text)
        self.parent.code_selection(text)
        self.close()
