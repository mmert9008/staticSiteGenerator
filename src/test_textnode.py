import unittest

# Assuming the TextNode and TextType are in textnode.py within the src directory
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    """
    Unit tests for the TextNode class.
    """

    def test_eq(self):
        """
        Tests equality of two identical TextNode objects with default URL (None).
        """
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        """
        Tests equality of two identical TextNode objects including URL.
        """
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        """
        Tests inequality when text content is different.
        """
        node = TextNode("This is node 1", TextType.TEXT)
        node2 = TextNode("This is node 2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        """
        Tests inequality when text type is different.
        """
        node = TextNode("This is a node", TextType.TEXT)
        node2 = TextNode("This is a node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        """
        Tests inequality when URLs are different.
        """
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://www.bing.com")
        self.assertNotEqual(node, node2)

    def test_eq_url_is_none(self):
        """
        Tests equality when one node has URL=None explicitly and the other uses the default.
        """
        node = TextNode("Text node", TextType.TEXT, None)
        node2 = TextNode("Text node", TextType.TEXT) # url defaults to None
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()

