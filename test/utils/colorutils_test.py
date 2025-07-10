import unittest
import ocaqda.utils.colorutils as colorutils

class ColorUtilsTest(unittest.TestCase):
    def test_standard_background_color(self):
        self.assertEqual(colorutils.STANDARD_BACKGROUND_COLOR, "#FFFFFF")
    def test_highlight_color(self):
        self.assertEqual(colorutils.HIGHLIGHT_COLOR, "#FFCCCC")

if __name__ == '__main__':
    unittest.main() 