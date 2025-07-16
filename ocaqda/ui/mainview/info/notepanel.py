"""
Panel on the right side of the screen displaying notes
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class NotePanel(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.note = None
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
        self.note_area = QTextEdit()
        layout.addWidget(self.info_label)

        note_header_label = QLabel("Notes:")
        note_header_label.setStyleSheet(header_style)

        self.note_instruction_label = QLabel(
            "Please select a file or a code to attach notes")
        self.note_instruction_label.setWordWrap(True)

        layout.addWidget(note_header_label)
        layout.addWidget(self.note_instruction_label)
        layout.addWidget(self.note_area)
        self.setLayout(layout)

    def set_selected_item_info(self, id, name, type):
        self.save_current_note()

        self.selected_item = [id, type]
        self.info_label.setText("Selected " + type + " : " + name)
        self.note_instruction_label.setText("")

        self.note_area.clear()
        self.load_note(id)

    def load_note(self, id):
        if self.selected_item[1] == "code":
            note = self.load_note_for_code(id)
            if note is not None:
                self.note_area.setText(note.text)
        else:
            note = self.load_note_for_file(id)
            if note is not None:
                self.note_area.setText(note.text)

    def save_current_note(self):
        if self.selected_item is not None:
            if self.selected_item[1] == "code":
                self.save_note_for_code(self.selected_item[0])
            elif self.selected_item[1] == "file":
                self.save_note_for_file(self.selected_item[0])

    def load_note_for_code(self, id):
        if self.selected_item is not None:
            if self.selected_item[1] == "code":
                self.note = self.main_window.project_service.load_note_for_code(id)
                if self.note is not None:
                    self.note_area.setText(self.note.text)

    def load_note_for_file(self, id):
        if self.selected_item is not None:
            if self.selected_item[1] == "file":
                self.note = self.main_window.project_service.load_note_for_file(id)
                if self.note is not None:
                    self.note_area.setText(self.note.text)

    def save_note_for_code(self, id):
        self.main_window.project_service.save_note_for_code(id, self.note_area.toPlainText())

    def save_note_for_file(self, id):
        self.main_window.project_service.save_note_for_file(id, self.note_area.toPlainText())
