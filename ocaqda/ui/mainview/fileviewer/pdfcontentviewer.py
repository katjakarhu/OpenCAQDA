"""
This component displays PDF content. The PDF file is stored as a binary to database, see DataFile.file_content

"""

from PySide6.QtCore import QByteArray, QBuffer, QIODevice, Slot, QPoint, Signal
from PySide6.QtGui import Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView


class PDFContentViewer(QPdfView):
    pageChanged = Signal(int)  # Signal emitted when page changes

    def __init__(self, parent, datafile):
        super(PDFContentViewer, self).__init__(parent)
        self.parent = parent
        self.data_file = datafile
        self.document = QPdfDocument()
        self.file_content = self.load_binary_file_content(datafile)
        ba = QByteArray(self.file_content)
        self.device = QBuffer(ba)
        self.device.open(QIODevice.OpenModeFlag.ReadOnly)
        self.document.load(self.device)
        self.setDocument(self.document)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        if self.document.pageCount() == 1:
            self.setPageMode(QPdfView.PageMode.SinglePage)
        else:
            self.setPageMode(QPdfView.PageMode.MultiPage)


    def load_binary_file_content(self, datafile):
        return self.parent.project_service.load_binary_file_content(datafile)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            pass

        super().mousePressEvent(e)

    def on_action_previous_page_triggered(self):
        nav = self.pageNavigator()
        nav.jump(nav.currentPage() - 1, QPoint(), nav.currentZoom())

    @Slot()
    def on_action_next_page_triggered(self):
        nav = self.pageNavigator()
        nav.jump(nav.currentPage() + 1, QPoint(), nav.currentZoom())

    def closeEvent(self, event):
        self.device.close()
        super().closeEvent(event)
