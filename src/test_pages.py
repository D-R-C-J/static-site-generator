import unittest

from pages import extract_title



class TestMain(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# My Title\n\nThis is some content."
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")

    def test_extract_title_no_title(self):
        markdown = "This is some content."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in markdown. Title must be the first line and start with '# '")
