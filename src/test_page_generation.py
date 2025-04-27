import unittest
# Import the function to test
from markdown_utils import extract_title

# Unit tests for page generation related functions.
class TestPageGeneration(unittest.TestCase):

    # --- extract_title tests ---

    # Tests extracting a basic H1 title.
    def test_extract_title_basic(self):
        md = "# This is a title"
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    # Tests extracting H1 title with leading/trailing whitespace around #.
    def test_extract_title_whitespace_around_hash(self):
        md = "  #   Title with whitespace  "
        title = extract_title(md)
        self.assertEqual(title, "Title with whitespace") # Whitespace around text should also be stripped

    # Tests extracting H1 title with leading/trailing whitespace in the text.
    def test_extract_title_whitespace_in_text(self):
        md = "#   My Title   "
        title = extract_title(md)
        self.assertEqual(title, "My Title")

    # Tests markdown with other heading levels but no H1.
    def test_extract_title_no_h1(self):
        md = """
## Not an H1
### Also not H1

Some text.
"""
        with self.assertRaisesRegex(ValueError, "Markdown must contain an H1 header"):
            extract_title(md)

    # Tests markdown with text before the H1.
    def test_extract_title_text_before_h1(self):
        md = """
Some introductory text.

# The Real Title

More text.
"""
        title = extract_title(md)
        self.assertEqual(title, "The Real Title")

    # Tests markdown with no headings at all.
    def test_extract_title_no_headings(self):
        md = """
Just a paragraph.

Another paragraph.
"""
        with self.assertRaisesRegex(ValueError, "Markdown must contain an H1 header"):
            extract_title(md)

    # Tests markdown with an empty H1 title.
    def test_extract_title_empty_h1(self):
        md = "# "
        title = extract_title(md)
        self.assertEqual(title, "")

    # Tests markdown with H1 followed by other lines (should only take the first H1 line).
    def test_extract_title_h1_with_more_lines(self):
        md = """
# The Title Line
This is not part of the title.
"""
        title = extract_title(md)
        self.assertEqual(title, "The Title Line")

    # Tests markdown with multiple H1 headers (should take the first).
    def test_extract_title_multiple_h1s(self):
        md = """
# First H1 (Should be taken)

# Second H1 (Should be ignored)
"""
        title = extract_title(md)
        self.assertEqual(title, "First H1 (Should be taken)")


if __name__ == "__main__":
    unittest.main()

