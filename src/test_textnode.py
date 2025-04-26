import unittest

# Import everything needed from textnode.py
from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter, # Correctly import from textnode
    text_to_textnodes,
)
# Import LeafNode from htmlnode.py
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    """
    Unit tests for the TextNode class and related functions.
    """

    # --- TextNode equality tests (Keep existing tests) ---

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


    # --- text_node_to_html_node tests (Keep existing tests) ---

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
        class UnknownTextType:
            value = "unknown"
        node = TextNode("Some text", UnknownTextType())

        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertIn("Invalid text type:", str(cm.exception))

    # --- split_nodes_delimiter tests (Keep existing tests) ---

    def test_split_one_delimiter(self):
        """
        Tests splitting with one pair of delimiters.
        """
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_split_multiple_delimiters(self):
        """
        Tests splitting with multiple pairs of the same delimiter.
        """
        node = TextNode("`code1` text `code2` more text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 4) # Corrected expected length
        self.assertEqual(new_nodes[0], TextNode("code1", TextType.CODE))
        self.assertEqual(new_nodes[1], TextNode(" text ", TextType.TEXT))
        self.assertEqual(new_nodes[2], TextNode("code2", TextType.CODE))
        self.assertEqual(new_nodes[3], TextNode(" more text", TextType.TEXT))

    def test_split_delimiter_at_start_and_end(self):
        """
        Tests splitting when the delimiter is at the beginning and end of the text.
        """
        node = TextNode("`code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("code block", TextType.CODE))

    def test_split_delimiter_only(self):
        """
        Tests splitting with only delimiters and no content.
        """
        node = TextNode("``", TextType.TEXT) # Represents an empty code block
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("", TextType.CODE))

    def test_split_multiple_nodes_mixed_types(self):
        """
        Tests splitting a list containing mixed node types.
        Only TEXT nodes should be split.
        """
        node1 = TextNode("text **bold** text", TextType.TEXT)
        node2 = TextNode("already bold", TextType.BOLD)
        node3 = TextNode("more text _italic_ text", TextType.TEXT)
        node4 = TextNode("already code", TextType.CODE)

        old_nodes = [node1, node2, node3, node4]
        # First split by bold
        nodes_after_bold = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(nodes_after_bold), 6)

        self.assertEqual(nodes_after_bold[0], TextNode("text ", TextType.TEXT))
        self.assertEqual(nodes_after_bold[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes_after_bold[2], TextNode(" text", TextType.TEXT))
        self.assertEqual(nodes_after_bold[3], node2)
        self.assertEqual(nodes_after_bold[4], node3)
        self.assertEqual(nodes_after_bold[5], node4)

        # Then split the result by italic
        nodes_after_italic = split_nodes_delimiter(nodes_after_bold, "_", TextType.ITALIC)
        self.assertEqual(len(nodes_after_italic), 8)

        self.assertEqual(nodes_after_italic[0], nodes_after_bold[0])
        self.assertEqual(nodes_after_italic[1], nodes_after_bold[1])
        self.assertEqual(nodes_after_italic[2], nodes_after_bold[2])
        self.assertEqual(nodes_after_italic[3], nodes_after_bold[3])
        self.assertEqual(nodes_after_italic[4], TextNode("more text ", TextType.TEXT))
        self.assertEqual(nodes_after_italic[5], TextNode("italic", TextType.ITALIC))
        self.assertEqual(nodes_after_italic[6], TextNode(" text", TextType.TEXT))
        self.assertEqual(nodes_after_italic[7], nodes_after_bold[5])


    def test_split_no_delimiter(self):
        """
        Tests splitting when the delimiter is not present.
        """
        node = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_split_unbalanced_delimiter(self):
        """
        Tests that a ValueError is raised for unbalanced delimiters.
        """
        node = TextNode("This is text with a `code block word", TextType.TEXT) # Missing closing backtick
        with self.assertRaisesRegex(ValueError, "Invalid Markdown syntax: Unbalanced delimiter"):
            split_nodes_delimiter([node], "`", TextType.CODE)

        node2 = TextNode("`code block` word `", TextType.TEXT) # Missing closing backtick
        with self.assertRaisesRegex(ValueError, "Invalid Markdown syntax: Unbalanced delimiter"):
            split_nodes_delimiter([node2], "`", TextType.CODE)

        node3 = TextNode("text `code` text `more", TextType.TEXT) # Odd number of delimiters
        with self.assertRaisesRegex(ValueError, "Invalid Markdown syntax: Unbalanced delimiter"):
             split_nodes_delimiter([node3], "`", TextType.CODE)


    def test_split_empty_list(self):
        """
        Tests splitting an empty list.
        """
        new_nodes = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 0)
        self.assertEqual(new_nodes, [])

    # --- text_to_textnodes tests ---

    def test_text_to_textnodes_all_types(self):
        """
        Tests converting text with all inline types. (Provided example)
        """
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected_nodes, text_to_textnodes(text))

    def test_text_to_textnodes_no_special_syntax(self):
        """
        Tests converting text with no special inline syntax.
        """
        text = "This is just plain text."
        expected_nodes = [TextNode("This is just plain text.", TextType.TEXT)]
        self.assertListEqual(expected_nodes, text_to_textnodes(text))

    def test_text_to_textnodes_only_one_type(self):
        """
        Tests converting text with only one type of inline syntax (e.g., only bold).
        """
        text = "This is **bold** text."
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertListEqual(expected_nodes, text_to_textnodes(text))

    def test_text_to_textnodes_multiple_of_one_type(self):
        """
        Tests converting text with multiple instances of the same type (e.g., two code blocks).
        """
        text = "Code `block1` and `block2` here."
        expected_nodes = [
            TextNode("Code ", TextType.TEXT),
            TextNode("block1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("block2", TextType.CODE),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertListEqual(expected_nodes, text_to_textnodes(text))

    def test_text_to_textnodes_mixed_order(self):
        """
        Tests converting text with mixed types in a different order than the example.
        """
        text = "`code` first, then **bold**, then _italic_."
        expected_nodes = [
            TextNode("code", TextType.CODE),
            TextNode(" first, then ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(expected_nodes, text_to_textnodes(text))

    def test_text_to_textnodes_empty_string(self):
        """
        Tests converting an empty string.
        """
        text = ""
        expected_nodes = []
        self.assertListEqual(expected_nodes, text_to_textnodes(text))


if __name__ == "__main__":
    unittest.main()
