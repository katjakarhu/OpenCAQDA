"""
PDFViewer displays the original PDF (PDFContentViewer) and plain text version (textviewer) side by side.
This is because Qt's PDF implementation does not directly support selecting text.

To enable the drag and drop coding for selected text in PDF, the alternative was to display the text-only version
side-by-side with the original PDF. Original PDF may contain important contextual information such as figures that
lost with the text conversion, therefore it was important to have it visible as well.

"""
from PySide6.QtCore import QPoint
from PySide6.QtGui import QTextCursor
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

        layout.addWidget(self.text_content)
        layout.addWidget(self.pdf_content)

        self.setLayout(layout)

        # Connect scroll signals
        self.text_content.verticalScrollBar().valueChanged.connect(self.on_text_scrolled)
        self.pdf_content.verticalScrollBar().valueChanged.connect(self.on_pdf_scrolled)

    def on_text_scrolled(self, value):
        """
        If the cursor is on the text content side, then we know that the text is scrolled
        """
        if self.cursor().pos().x() <= self.text_content.viewport().rect().topRight().x():

            # Calculate the cursor position based on the scroll value
            cursor = self.text_content.cursorForPosition(
                self.text_content.viewport().mapFrom(self.text_content, self.text_content.viewport().rect().topLeft()))

            cursor.movePosition(QTextCursor.MoveOperation.Down)

            # Set the text cursor
            self.text_content.setTextCursor(cursor)

            position = cursor.position()

            page_index = self.text_content.toPlainText().rfind('Page ', 0, position)

            if page_index != -1:
                page_number_string = self.text_content.toPlainText()[page_index + 5:page_index + 15:]
                page_number = str()
                for c in page_number_string:
                    if c.isdigit():
                        page_number = page_number + c
                    else:
                        break

                self.pdf_content.pageNavigator().jump(int(page_number), QPoint(),
                                                      self.pdf_content.pageNavigator().currentZoom())

    def on_pdf_scrolled(self, value):
        """
        If cursor is on the PDF content side, then the PDF is scrolled
        """
        if self.cursor().pos().x() > self.text_content.viewport().rect().topRight().x():
            cursor = self.text_content.textCursor()
            page = self.pdf_content.pageNavigator().currentPage()
            # Calculate approximate text position based on page number
            # This assumes text content is roughly divided equally among pages
            total_pages = self.pdf_content.document.pageCount()
            text_length = len(self.text_content.toPlainText())
            chars_per_page = text_length / total_pages
            target_position = int(page * chars_per_page)

            # Scroll text to the calculated position
            cursor.setPosition(target_position)
            self.text_content.setTextCursor(cursor)
            self.text_content.ensureCursorVisible()
