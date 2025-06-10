from PySide6.QtCore import QByteArray, QBuffer, QIODevice
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView


class PDFViewer(QPdfView):
    def __init__(self, parent, datafile):
        super(PDFViewer, self).__init__(parent)
        self.parent = parent
        self.data_file = datafile
        self.document = QPdfDocument()
        self.file_content = self.load_binary_file_content(datafile)
        ba = QByteArray(self.file_content)
        device = QBuffer(ba)
        device.open(QIODevice.OpenModeFlag.ReadOnly)
        self.document.load(device)
        device.close()
        self.setDocument(self.document)

    def load_binary_file_content(self, datafile):
        return self.parent.project_manager.load_binary_file_content(datafile)
