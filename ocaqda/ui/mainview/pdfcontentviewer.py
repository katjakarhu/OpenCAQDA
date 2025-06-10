from PySide6.QtCore import QByteArray, QBuffer, QIODevice, Slot, QPoint
from PySide6.QtGui import Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView


class PDFContentViewer(QPdfView):
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
        # device.close()
        self.setDocument(self.document)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)
        if self.document.pageCount() == 1:
            self.setPageMode(QPdfView.PageMode.SinglePage)
        else:
            self.setPageMode(QPdfView.PageMode.MultiPage)

        nav = self.pageNavigator()

    def load_binary_file_content(self, datafile):
        return self.parent.project_manager.load_binary_file_content(datafile)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            pass

        super().mousePressEvent(e)

    def on_actionPrevious_Page_triggered(self):
        nav = self.pageNavigator()
        nav.jump(nav.currentPage() - 1, QPoint(), nav.currentZoom())

    @Slot()
    def on_actionNext_Page_triggered(self):
        nav = self.pageNavigator()
        nav.jump(nav.currentPage() + 1, QPoint(), nav.currentZoom())

    def closeEvent(self, event):
        self.device.close()
        super().closeEvent(event)
