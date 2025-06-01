from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class InfoAndNotePanel(QWidget):
    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        layout = QVBoxLayout()
        info_header_label = QLabel("Information:")
        header_style = "font-size: 14px; font-weight: bold;"
        info_header_label.setStyleSheet(header_style)
        layout.addWidget(info_header_label)

        # Description text
        info_label = QLabel(
            "Info here"
        )
        info_label.setWordWrap(True)
        info_label.setMaximumWidth(380)
        info_label.setMinimumHeight(100)
        self.info_label = QLabel("Info")
        self.note_area = QTextEdit("jdksjdksak")
        layout.addWidget(self.info_label)

        note_header_label = QLabel("Notes:")
        note_header_label.setStyleSheet(header_style)

        note_instruction_label = QLabel(
            "Please select a file or a code to attach notes to. You can view and export notes from the tools menu")
        note_instruction_label.setWordWrap(True)

        layout.addWidget(note_header_label)
        layout.addWidget(note_instruction_label)
        layout.addWidget(self.note_area)
        self.setLayout(layout)
