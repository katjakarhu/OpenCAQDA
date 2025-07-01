"""
This component displays PDF content. The PDF file is stored as a binary to database, see DataFile.file_content

"""

from PySide6.QtCore import QByteArray, QBuffer, QIODevice, Signal
from PySide6.QtGui import Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView


class PDFContentViewer(QPdfView):
    pageChanged = Signal(int)  # Signal emitted when page changes

    def __init__(self, parent, main_window, datafile):
        super(PDFContentViewer, self).__init__(parent)
        self.ba = None
        self.device = None
        self.parent = parent
        self.main_window = main_window
        self.data_file = datafile
        self.document = QPdfDocument()
        self.set_bytearray_to_document(datafile)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)

        if self.document.pageCount() == 1:
            self.setPageMode(QPdfView.PageMode.SinglePage)
        else:
            self.setPageMode(QPdfView.PageMode.MultiPage)

    def set_bytearray_to_document(self, datafile):
        file_content = self.load_binary_file_content(datafile)
        self.ba = QByteArray(file_content)
        self.device = QBuffer(self.ba)
        self.device.open(QIODevice.OpenModeFlag.ReadOnly)
        self.document.load(self.device)
        self.setDocument(self.document)

    def load_binary_file_content(self, datafile):
        return self.main_window.project_service.load_binary_file_content(datafile)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            pass

        super().mousePressEvent(e)

    def closeEvent(self, event):
        self.device.close()
        super().closeEvent(event)
