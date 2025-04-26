#!/usr/bin/env python3

from enum import Enum
from htmlnode import LeafNode
# Import splitting functions that are in markdown_utils
from markdown_utils import split_nodes_image, split_nodes_link


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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: Unbalanced delimiter '{delimiter}' in text: {node.text}")

        for i in range(len(parts)):
            part = parts[i]
            if i % 2 == 0:
                if part != "":
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def text_to_textnodes(text):
    # These splitting functions operate sequentially
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)         # Lives in markdown_utils
    nodes = split_nodes_link(nodes)          # Lives in markdown_utils
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD) # Lives in textnode
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  # Lives in textnode
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)   # Lives in textnode
    return nodes

