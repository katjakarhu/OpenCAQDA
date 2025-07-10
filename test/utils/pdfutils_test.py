import unittest
from unittest.mock import patch, mock_open
from ocaqda.utils import pdfutils

class PdfUtilsTest(unittest.TestCase):
    @patch('ocaqda.utils.pdfutils.extract_text_to_fp')
    @patch('builtins.open', new_callable=mock_open, read_data=b'%PDF-1.4')
    def test_convert_pdf_to_html(self, mock_file, mock_extract):
        mock_extract.side_effect = lambda f, out, **kwargs: out.write('<html>PDF</html>')
        result = pdfutils.convert_pdf_to_html('dummy.pdf')
        self.assertEqual(result, '<html>PDF</html>')
        mock_file.assert_called_once_with('dummy.pdf', 'rb')
        mock_extract.assert_called()

if __name__ == '__main__':
    unittest.main() 