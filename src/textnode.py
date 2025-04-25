#!/usr/bin/env python3

from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({repr(self.text)}, {repr(self.text_type.value)}, {repr(self.url)})"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Invalid text type: {text_node.text_type}")

def main():
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    print(html_node)

    link_node = TextNode("Google Link", TextType.LINK, "https://www.google.com")
    html_link_node = text_node_to_html_node(link_node)
    print(html_link_node)

    img_node = TextNode("Python Logo", TextType.IMAGE, "https://www.python.org/static/logo.png")
    html_img_node = text_node_to_html_node(img_node)
    print(html_img_node)


if __name__ == "__main__":
    main()

