import unittest

# Assuming TextNode, TextType, and text_node_to_html_node are in textnode.py within the src directory
# Also assuming LeafNode is defined in htmlnode.py within the src directory
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode # Import LeafNode


class TestTextNode(unittest.TestCase):
    """
    Unit tests for the TextNode class and the text_node_to_html_node function.
    """

    # --- TextNode equality tests ---

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

    def test_not_eq_url_none_vs_value(self):
        """
        Tests inequality when one node has a URL and the other has URL=None.
        """
        node = TextNode("Link", TextType.LINK, "http://example.com")
        node2 = TextNode("Link", TextType.LINK, None)
        self.assertNotEqual(node, node2)


    # --- text_node_to_html_node tests ---

    def test_text_node_to_html_node_text(self):
        """
        Tests conversion of TextType.TEXT.
        """
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode) # Check it's a LeafNode
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None) # Ensure no props

    def test_text_node_to_html_node_bold(self):
        """
        Tests conversion of TextType.BOLD.
        """
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode) # Check it's a LeafNode
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None) # Ensure no props

    def test_text_node_to_html_node_italic(self):
        """
        Tests conversion of TextType.ITALIC.
        """
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode) # Check it's a LeafNode
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None) # Ensure no props

    def test_text_node_to_html_node_code(self):
        """
        Tests conversion of TextType.CODE.
        """
        node = TextNode("code block", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode) # Check it's a LeafNode
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code block")
        self.assertEqual(html_node.props, None) # Ensure no props

    def test_text_node_to_html_node_link(self):
        """
        Tests conversion of TextType.LINK.
        """
        node = TextNode("Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode) # Check it's a LeafNode
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google") # Anchor text is the value
        self.assertEqual(html_node.props, {"href": "https://www.google.com"}) # URL is href prop

    def test_text_node_to_html_node_image(self):
        """
        Tests conversion of TextType.IMAGE.
        """
        node = TextNode("Python Logo", TextType.IMAGE, "https://www.python.org/static/logo.png")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode) # Check it's a LeafNode
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "") # Value should be empty string for images
        self.assertEqual(html_node.props, {"src": "https://www.python.org/static/logo.png", "alt": "Python Logo"}) # URL is src prop, text is alt prop

    def test_text_node_to_html_node_raises_error(self):
        """
        Tests that text_node_to_html_node raises ValueError for invalid text type.
        """
        # Create a dummy node with a non-existent text type value
        class UnknownTextType:
            value = "unknown"

        node = TextNode("Some text", UnknownTextType())

        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertIn("Invalid text type:", str(cm.exception))


if __name__ == "__main__":
    unittest.main()

