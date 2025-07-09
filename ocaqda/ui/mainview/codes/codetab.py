"""
A tab on left side of the screen that displays the codes

Right mouse button: Codes can be arranged to a hierarchy by drag and drop

Left mouse button: Coding is done by dragging the code over a selected text in the center text component

"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, \
    QHBoxLayout

from ocaqda.ui.mainview.codes.codetree import CodeTree


class CodeTab(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        analysis_layout = QVBoxLayout()
        # Tree widget for analysis tab
        self.code_tree = CodeTree(main_window, self)
        self.filter_field = QLineEdit()
        self.filter_field.setPlaceholderText("Filter codes...")

        self.filter_field.textChanged.connect(self.code_tree.filter_codes)
        analysis_layout.addWidget(self.filter_field)

        analysis_layout.addWidget(self.code_tree)

        # Button to add new text entries
        add_code_layout = QHBoxLayout()
        self.add_code_field = QLineEdit()
        self.add_button = QPushButton("Add code")
        self.add_button.clicked.connect(self.add_and_save_code)
        add_code_layout.addWidget(self.add_code_field)
        add_code_layout.addWidget(self.add_button)
        analysis_layout.addLayout(add_code_layout)

        self.manage_codes_button = QPushButton("Manage codes")
        self.manage_codes_button.clicked.connect(self.manage_codes)
        analysis_layout.addWidget(self.manage_codes_button)
        self.setLayout(analysis_layout)

    def manage_codes(self):
        raise "Implement me!"

    def add_and_save_code(self):
        text = self.add_code_field.text()
        self.code_tree.add_and_save_code(text)
