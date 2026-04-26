from PyQt6.QtWidgets import QFileDialog


class ExportDialog(QFileDialog):
    def __init__(self, parent=None, project_service=None, export_type=None):
        QFileDialog.__init__(self, parent)
        self.project_service = project_service
        self.export_type = export_type
        self.set_window_title()

        # Set default file mode and accept mode
        self.setFileMode(QFileDialog.FileMode.AnyFile)
        self.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)

        # Connect the fileSelected signal to handle the export
        self.fileSelected.connect(self._handle_export)

    def set_window_title(self):
        if self.export_type == "code":
            self.setWindowTitle("Export codes")
        elif self.export_type == "memo":
            self.setWindowTitle("Export memos")
        else:
            raise Exception("Invalid export type")

    def _handle_export(self, file_path: str):
        """Called when a file is selected. Fetches data and saves it to the file."""
        if self.export_type == "code":
           print(self.project_service.get_project_codes())




    def show_dialog(self):
        """Show the dialog and return True if export succeeded, False otherwise."""
        if self.exec() == QFileDialog.accepted:
            return True
        return False



