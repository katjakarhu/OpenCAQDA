import unittest
import ocaqda.utils.constants as constants

class ConstantsTest(unittest.TestCase):
    def test_configuration_file_name(self):
        self.assertEqual(constants.CONFIGURATION_FILE_NAME, "opencaqda-settings.yaml")
    def test_pdf_file_extension(self):
        self.assertEqual(constants.PDF_FILE_EXTENSION, ".pdf")
    def test_text_file_extension(self):
        self.assertEqual(constants.TEXT_FILE_EXTENSION, ".txt")

if __name__ == '__main__':
    unittest.main() 