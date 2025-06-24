"""
PDFViewer displays the original PDF (PDFContentViewer) and plain text version (textviewer) side by side.
This is because Qt's PDF implementation does not directly support selecting text.

To enable the drag and drop coding for selected text in PDF, the alternative was to display the text-only version
side-by-side with the original PDF. Original PDF may contain important contextual information such as figures that
lost with the text conversion, therefore it was important to have it visible as well.

"""

from PySide6.QtWidgets import QWidget, QHBoxLayout

from ocaqda.ui.mainview.fileviewer.htmlviewer import HTMLViewer
from ocaqda.ui.mainview.fileviewer.pdfcontentviewer import PDFContentViewer


class PDFViewer(QWidget):
    def __init__(self, parent, datafile):
        super(PDFViewer, self).__init__(parent)
        self.parent = parent
        self.datafile = datafile

        layout = QHBoxLayout()
        self.pdf_content = PDFContentViewer(parent, datafile)
        self.text_content = HTMLViewer(parent, datafile)

        # Connect scroll signals
        self.pdf_content.pageChanged.connect(self.on_pdf_page_changed)
        self.text_content.verticalScrollBar().valueChanged.connect(self.on_text_scrolled)

        layout.addWidget(self.text_content)
        layout.addWidget(self.pdf_content)

        self.setLayout(layout)

    def on_pdf_page_changed(self, page):
        # Calculate approximate text position based on page number
        # This assumes text content is roughly divided equally among pages
        total_pages = self.pdf_content.document.pageCount()
        text_length = len(self.text_content.toPlainText())
        chars_per_page = text_length / total_pages
        target_position = int(page * chars_per_page)

        # Scroll text to the calculated position
        cursor = self.text_content.textCursor()
        cursor.setPosition(target_position)
        self.text_content.setTextCursor(cursor)
        self.text_content.ensureCursorVisible()

    def on_text_scrolled(self, value):
        # Calculate approximate page number based on scroll position
        text_length = len(self.text_content.toPlainText())
        total_pages = self.pdf_content.document.pageCount()
        chars_per_page = text_length / total_pages

        # Get current cursor position
        cursor_pos = self.text_content.textCursor().position()
        target_page = int(cursor_pos / chars_per_page)

        # Update PDF view if page changed
        if target_page != self.pdf_content.pageNavigator().currentPage():
            self.pdf_content.pageNavigator().jump(target_page, self.pdf_content.pageNavigator().currentLocation(),
                                                  self.pdf_content.pageNavigator().currentZoom())
