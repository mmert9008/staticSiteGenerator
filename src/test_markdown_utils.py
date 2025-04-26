import unittest

# Assuming TextNode, TextType are in textnode.py
from textnode import TextNode, TextType

# Assuming extract_markdown_images, extract_markdown_links,
# split_nodes_image, and split_nodes_link are in markdown_utils.py
from markdown_utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)


class TestMarkdownUtils(unittest.TestCase):
    """
    Unit tests for Markdown utility functions.
    """

    # --- Extraction Tests (Keep existing tests) ---

    def test_extract_markdown_images_basic(self):
        """
        Tests extracting a single image.
        """
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        """
        Tests extracting multiple images.
        """
        text = "![image1](url1) text ![image2](url2) more text"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image1", "url1"), ("image2", "url2")], matches)

    def test_extract_markdown_images_no_match(self):
        """
        Tests extracting images when none are present.
        """
        text = "This is text with no images or links."
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_at_edges(self):
        """
        Tests extracting images at the beginning and end of the text.
        """
        text = "![start](start_url) text ![end](end_url)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("start", "start_url"), ("end", "end_url")], matches)

    def test_extract_markdown_images_empty_alt_text(self):
        """
        Tests extracting images with empty alt text.
        """
        text = "Text with an ![](/path/to/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "/path/to/image.png")], matches)

    def test_extract_markdown_images_empty_url(self):
        """
        Tests extracting images with empty URL (regex should handle this).
        """
        text = "Text with ![alttext]()"
        matches = extract_markdown_images(text)
        self.assertListEqual([("alttext", "")], matches)

    def test_extract_markdown_images_with_links(self):
        """
        Tests that image extraction ignores link syntax.
        """
        text = "![image](image.png) and a [link](link.html)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "image.png")], matches)


    def test_extract_markdown_links_basic(self):
        """
        Tests extracting a single link.
        """
        text = "This is text with a [link](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        """
        Tests extracting multiple links.
        """
        text = "[link1](url1) text [link2](url2) more text"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link1", "url1"), ("link2", "url2")], matches)

    def test_extract_markdown_links_no_match(self):
        """
        Tests extracting links when none are present (and no images).
        """
        text = "This is just text with no special syntax."
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_at_edges(self):
        """
        Tests extracting links at the beginning and end of the text.
        """
        text = "[start](start_url) text [end](end_url)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("start", "start_url"), ("end", "end_url")], matches)

    def test_extract_markdown_links_empty_anchor_text(self):
        """
        Tests extracting links with empty anchor text.
        """
        text = "Text with an [](/path/to/page.html)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "/path/to/page.html")], matches)

    def test_extract_markdown_links_empty_url(self):
        """
        Tests extracting links with empty URL.
        """
        text = "Text with [anchortext]()"
        matches = extract_markdown_links(text)
        self.assertListEqual([("anchortext", "")], matches)

    def test_extract_markdown_links_ignores_images(self):
        """
        Tests that link extraction ignores image syntax.
        """
        text = "A [link](link.html) and an ![image](image.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "link.html")], matches)

    def test_extract_markdown_links_and_images_mixed(self):
        """
        Tests that link extraction works correctly when images are also present.
        """
        text = "![image](image.png) and a [link](link.html) and another ![img2](url2)"
        matches_links = extract_markdown_links(text)
        self.assertListEqual([("link", "link.html")], matches_links)
        matches_images = extract_markdown_images(text)
        self.assertListEqual([("image", "image.png"), ("img2", "url2")], matches_images)


    # --- Split Image Tests ---

    def test_split_images(self):
        """
        Tests splitting text with multiple images. (Provided test)
        """
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        """
        Tests splitting text with a single image.
        """
        node = TextNode("Text before ![image](url) text after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_start(self):
        """
        Tests splitting text with an image at the beginning.
        """
        node = TextNode("![image](url) text after", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        """
        Tests splitting text with an image at the end.
        """
        node = TextNode("Text before ![image](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url"),
            ],
            new_nodes,
        )

    def test_split_images_only(self):
        """
        Tests splitting text that contains only an image.
        """
        node = TextNode("![image](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("image", TextType.IMAGE, "url")], new_nodes)

    def test_split_images_adjacent(self):
        """
        Tests splitting text with adjacent images.
        """
        node = TextNode("![img1](url1)![img2](url2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode("img2", TextType.IMAGE, "url2"),
            ],
            new_nodes,
        )

    def test_split_images_empty_alt_or_url(self):
        """
        Tests splitting images with empty alt text or URL.
        """
        node = TextNode("Text ![](/path.png) ![]( ) text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "/path.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("", TextType.IMAGE, " "),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_images_no_images(self):
        """
        Tests splitting text with no images.
        """
        node = TextNode("This is just text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes) # Original node should be returned unchanged

    def test_split_images_mixed_list(self):
        """
        Tests splitting a list with mixed node types.
        Non-TEXT nodes should pass through unchanged.
        """
        node1 = TextNode("Text with ![img1](u1)", TextType.TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("![img2](u2) more text", TextType.TEXT)
        old_nodes = [node1, node2, node3]

        new_nodes = split_nodes_image(old_nodes)

        # Expected: [Text before img1, img1 node, node2 (passed through), img2 node, text after img2]
        self.assertEqual(len(new_nodes), 5) # node1 splits into 2, node2 passes through, node3 splits into 2
        self.assertEqual(new_nodes[0], TextNode("Text with ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("img1", TextType.IMAGE, "u1"))
        self.assertEqual(new_nodes[2], node2) # Bold node passed through
        self.assertEqual(new_nodes[3], TextNode("img2", TextType.IMAGE, "u2"))
        self.assertEqual(new_nodes[4], TextNode(" more text", TextType.TEXT)) # Trailing text from node3


    # --- Split Link Tests ---

    def test_split_links(self):
        """
        Tests splitting text with multiple links. (Similar to provided example)
        """
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_links_single(self):
        """
        Tests splitting text with a single link.
        """
        node = TextNode("Text before [link](url) text after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_start(self):
        """
        Tests splitting text with a link at the beginning.
        """
        node = TextNode("[link](url) text after", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        """
        Tests splitting text with a link at the end.
        """
        node = TextNode("Text before [link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
            new_nodes,
        )

    def test_split_links_only(self):
        """
        Tests splitting text that contains only a link.
        """
        node = TextNode("[link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("link", TextType.LINK, "url")], new_nodes)

    def test_split_links_adjacent(self):
        """
        Tests splitting text with adjacent links.
        """
        node = TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_split_links_empty_anchor_or_url(self):
        """
        Tests splitting links with empty anchor text or URL.
        """
        node = TextNode("Text [](/path.html) []( ) text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("", TextType.LINK, "/path.html"),
                TextNode(" ", TextType.TEXT),
                TextNode("", TextType.LINK, " "),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )


    def test_split_links_no_links(self):
        """
        Tests splitting text with no links (but may contain images).
        """
        node = TextNode("This is just text with no links but has an ![image](url).", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes) # Original node should be returned unchanged


    def test_split_links_mixed_list(self):
        """
        Tests splitting a list with mixed node types.
        Non-TEXT nodes should pass through unchanged.
        """
        node1 = TextNode("Text with [link1](u1)", TextType.TEXT)
        node2 = TextNode("Already italic", TextType.ITALIC)
        node3 = TextNode("[link2](u2) more text", TextType.TEXT)
        old_nodes = [node1, node2, node3]

        new_nodes = split_nodes_link(old_nodes)

        # Expected: [Text before link1, link1 node, node2 (passed through), link2 node, text after link2]
        self.assertEqual(len(new_nodes), 5) # node1 splits into 2, node2 passes through, node3 splits into 2
        self.assertEqual(new_nodes[0], TextNode("Text with ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("link1", TextType.LINK, "u1"))
        self.assertEqual(new_nodes[2], node2) # Italic node passed through
        self.assertEqual(new_nodes[3], TextNode("link2", TextType.LINK, "u2"))
        self.assertEqual(new_nodes[4], TextNode(" more text", TextType.TEXT)) # Trailing text from node3


    def test_split_links_and_images_combined(self):
        """
        Tests splitting a node with both links and images in the correct order.
        This tests sequential splitting (images first, then links on the resulting nodes).
        """
        node = TextNode("Text ![img](u1) text [link](u2) text ![img2](u3) text [link2](u4) text", TextType.TEXT)
        old_nodes = [node]

        # First split by images
        nodes_after_img_split = split_nodes_image(old_nodes)
        # Expected after image split:
        # [TextNode("Text ", TEXT), TextNode("img", IMAGE, "u1"), TextNode(" text [link](u2) text ", TEXT), TextNode("img2", IMAGE, "u3"), TextNode(" text [link2](u4) text", TEXT)]
        self.assertEqual(len(nodes_after_img_split), 5)
        self.assertEqual(nodes_after_img_split[0], TextNode("Text ", TextType.TEXT))
        self.assertEqual(nodes_after_img_split[1], TextNode("img", TextType.IMAGE, "u1"))
        self.assertEqual(nodes_after_img_split[2], TextNode(" text [link](u2) text ", TextType.TEXT)) # This node still contains link syntax
        self.assertEqual(nodes_after_img_split[3], TextNode("img2", TextType.IMAGE, "u3"))
        self.assertEqual(nodes_after_img_split[4], TextNode(" text [link2](u4) text", TextType.TEXT)) # This node still contains link syntax

        # Then split the result by links
        nodes_after_link_split = split_nodes_link(nodes_after_img_split)

        # Expected final nodes after both splits:
        self.assertEqual(len(nodes_after_link_split), 9) # Corrected expected length
        self.assertEqual(nodes_after_link_split[0], TextNode("Text ", TextType.TEXT)) # From the first split (before img1)
        self.assertEqual(nodes_after_link_split[1], TextNode("img", TextType.IMAGE, "u1")) # From the first split (img1 node)
        # The node " text [link](u2) text " from the first split gets split by link
        self.assertEqual(nodes_after_link_split[2], TextNode(" text ", TextType.TEXT)) # Before [link](u2)
        self.assertEqual(nodes_after_link_split[3], TextNode("link", TextType.LINK, "u2")) # The [link](u2) node
        self.assertEqual(nodes_after_link_split[4], TextNode(" text ", TextType.TEXT)) # After [link](u2) and before ![img2](u3)
        self.assertEqual(nodes_after_link_split[5], TextNode("img2", TextType.IMAGE, "u3")) # From the first split (img2 node)
        # The node " text [link2](u4) text" from the first split gets split by link
        self.assertEqual(nodes_after_link_split[6], TextNode(" text ", TextType.TEXT)) # Before [link2](u4)
        self.assertEqual(nodes_after_link_split[7], TextNode("link2", TextType.LINK, "u4")) # The [link2](u4) node
        self.assertEqual(nodes_after_link_split[8], TextNode(" text", TextType.TEXT)) # After [link2](u4)


if __name__ == "__main__":
    unittest.main()

