import unittest
from ocaqda.utils.general_utils import remove_html_tags

class GeneralUtilsTest(unittest.TestCase):
    def test_remove_html_tags(self):
        self.assertEqual(remove_html_tags('<b>bold</b>'), 'bold')
        self.assertEqual(remove_html_tags('no tags'), 'no tags')
        self.assertEqual(remove_html_tags('<div>hello <span>world</span></div>'), 'hello world')
        self.assertEqual(remove_html_tags(''), '')

if __name__ == '__main__':
    unittest.main() 