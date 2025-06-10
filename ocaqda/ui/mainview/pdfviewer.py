from PySide6.QtWidgets import QWidget, QHBoxLayout

from ocaqda.ui.mainview.pdfcontentviewer import PDFContentViewer
from ocaqda.ui.mainview.textviewer import TextViewer


class PDFViewer(QWidget):
    def __init__(self, parent, datafile):
        super(PDFViewer, self).__init__(parent)
        self.parent = parent
        self.datafile = datafile

        layout = QHBoxLayout()
        pdf_content = PDFContentViewer(parent, datafile)
        text_content = TextViewer(parent, datafile)

        layout.addWidget(pdf_content)
        layout.addWidget(text_content)

        self.setLayout(layout)
