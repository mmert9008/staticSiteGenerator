import unittest

# Assuming HTMLNode, LeafNode, and ParentNode are defined in htmlnode.py
from htmlnode import HTMLNode, LeafNode, ParentNode # ValueError is a built-in, no need to import from htmlnode


class TestHTMLNode(unittest.TestCase):
    """
    Unit tests for the HTMLNode and LeafNode classes.
    """

    # --- HTMLNode tests (Keep existing tests) ---
    # ... (your existing HTMLNode tests here) ...
    def test_props_to_html_basic(self):
        node = HTMLNode("a", "Link", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(
            "input",
            None,
            None,
            {"type": "text", "placeholder": "Enter name", "required": ""},
        )
        props_string = node.props_to_html()
        self.assertIn(' type="text"', props_string)
        self.assertIn(' placeholder="Enter name"', props_string)
        self.assertIn(' required=""', props_string)
        expected_length = len(' type="text"') + len(' placeholder="Enter name"') + len(' required=""')
        self.assertEqual(len(props_string), expected_length)

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Paragraph content", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("div", None, [], {})
        self.assertEqual(node.props_to_html(), "")

    # --- LeafNode tests (Keep existing tests) ---
    # ... (your existing LeafNode tests here) ...
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_div_props(self):
        node = LeafNode("div", "Content", {"class": "container", "id": "main"})
        generated_html = node.to_html()
        self.assertIn("<div", generated_html)
        self.assertIn(' class="container"', generated_html)
        self.assertIn(' id="main"', generated_html)
        self.assertIn(">Content</div>", generated_html)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some raw text.")
        self.assertEqual(node.to_html(), "Just some raw text.")

    def test_leaf_to_html_raises_error_no_value(self):
        with self.assertRaises(ValueError):
             LeafNode("p", None)


    # --- ParentNode tests (Add new tests) ---

    def test_to_html_with_children(self):
        """
        Tests ParentNode.to_html with a single LeafNode child.
        """
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        """
        Tests ParentNode.to_html with a nested ParentNode (grandchildren).
        """
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        """
        Tests ParentNode.to_html with multiple LeafNode children.
        """
        child1 = LeafNode("p", "Paragraph 1")
        child2 = LeafNode("span", "Span 1")
        child3 = LeafNode("b", "Bold 1")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>Paragraph 1</p><span>Span 1</span><b>Bold 1</b></div>",
        )

    def test_to_html_mixed_children(self):
        """
        Tests ParentNode.to_html with a mix of LeafNodes (with and without tags).
        """
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "Normal text")
        child3 = LeafNode("i", "italic text")
        child4 = LeafNode(None, "Another normal text")
        parent_node = ParentNode("p", [child1, child2, child3, child4])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Another normal text</p>",
        )

    def test_to_html_with_props(self):
        """
        Tests ParentNode.to_html with properties on the parent node.
        """
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "parent-container", "id": "main-div"})
        generated_html = parent_node.to_html()
        self.assertIn("<div", generated_html)
        self.assertIn(' class="parent-container"', generated_html)
        self.assertIn(' id="main-div"', generated_html)
        self.assertIn("><span>child</span></div>", generated_html)


    def test_to_html_raises_error_no_tag(self):
        """
        Tests that ParentNode raises ValueError if tag is None.
        """
        child_node = LeafNode("span", "child")
        with self.assertRaisesRegex(ValueError, "ParentNode requires a tag"):
             ParentNode(None, [child_node]).to_html() # Also test calling to_html after creation


    def test_to_html_raises_error_no_children(self):
        """
        Tests that ParentNode raises ValueError if children is None.
        """
        with self.assertRaisesRegex(ValueError, "ParentNode requires children"):
             ParentNode("div", None).to_html() # Test calling to_html after creation


    def test_to_html_raises_error_empty_children_list(self):
        """
        Tests that ParentNode raises ValueError if children is an empty list.
        """
        with self.assertRaisesRegex(ValueError, "ParentNode requires children"):
             ParentNode("div", []).to_html() # Test calling to_html after creation


if __name__ == "__main__":
    unittest.main()

