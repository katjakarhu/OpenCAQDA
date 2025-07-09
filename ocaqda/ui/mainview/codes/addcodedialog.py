from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QHBoxLayout


class AddCodeDialog(QDialog):
    def __init__(self, main_window, parent=None):
        super().__init__()
        self.main_window = main_window
        self.parent = parent

        self.setWindowTitle("Add code")
        self.setGeometry(100, 100, 400, 100)

        # Create QLineEdit
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("...")

        # Create QPushButton
        self.button = QPushButton("Add code", self)
        self.button.clicked.connect(self.on_button_click)

        # Create layout and add widgets
        layout = QHBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)

        # Set dialog layout
        self.setLayout(layout)

    def on_button_click(self):
        text = self.line_edit.text()
        if len(text) > 255:
            text = text[:255]

        self.main_window.code_tab.code_tree.add_and_save_code(text)
        self.parent.code_selection(text)
        self.close()
