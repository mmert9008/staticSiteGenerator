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


def main():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes1 = split_nodes_delimiter([node], "`", TextType.CODE)
    print("Example 1:")
    for node in new_nodes1:
        print(node)
    print("-" * 20)

    node2 = TextNode("Another `code` example", TextType.TEXT)
    node3 = TextNode("And some **bold** text", TextType.TEXT)
    combined_nodes = [node2, node3]
    print("Example 2 (before split):")
    for node in combined_nodes:
         print(node)
    print("-" * 20)

    nodes_after_code_split = split_nodes_delimiter(combined_nodes, "`", TextType.CODE)
    print("Example 2 (after code split):")
    for node in nodes_after_code_split:
        print(node)
    print("-" * 20)

    nodes_after_bold_split = split_nodes_delimiter(nodes_after_code_split, "**", TextType.BOLD)
    print("Example 2 (after bold split):")
    for node in nodes_after_bold_split:
        print(node)
    print("-" * 20)


if __name__ == "__main__":
    main()

