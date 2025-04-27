import re
from enum import Enum
import os
import shutil
import sys


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    from textnode import TextNode, TextType
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        last_end = 0
        current_nodes_for_this_text_node = []

        for match in re.finditer(image_regex, text):
            start, end = match.span()
            alt_text = match.group(1)
            url = match.group(2)

            if start > last_end:
                current_nodes_for_this_text_node.append(TextNode(text[last_end:start], TextType.TEXT))

            current_nodes_for_this_text_node.append(TextNode(alt_text, TextType.IMAGE, url))

            last_end = end

        if last_end < len(text):
            current_nodes_for_this_text_node.append(TextNode(text[last_end:], TextType.TEXT))

        if not current_nodes_for_this_text_node and not re.search(image_regex, text):
             new_nodes.append(node)
        else:
             new_nodes.extend(current_nodes_for_this_text_node)

    return new_nodes


def split_nodes_link(old_nodes):
    from textnode import TextNode, TextType
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        last_end = 0
        current_nodes_for_this_text_node = []

        for match in re.finditer(link_regex, text):
            start, end = match.span()
            anchor_text = match.group(1)
            url = match.group(2)

            if start > last_end:
                 current_nodes_for_this_text_node.append(TextNode(text[last_end:start], TextType.TEXT))

            current_nodes_for_this_text_node.append(TextNode(anchor_text, TextType.LINK, url))

            last_end = end

        if last_end < len(text):
            current_nodes_for_this_text_node.append(TextNode(text[last_end:], TextType.TEXT))

        if not current_nodes_for_this_text_node and not re.search(link_regex, text):
             new_nodes.append(node)
        else:
             new_nodes.extend(current_nodes_for_this_text_node)

    return new_nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            filtered_blocks.append(stripped_block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split('\n')

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    if re.match(r"#{1,6} ", block) and len(lines) == 1:
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    return BlockType.PARAGRAPH


def copy_contents_recursive(source_dir_path, dest_dir_path):
    print(f"Copying contents from {source_dir_path} to {dest_dir_path}")

    try:
        dir_contents = os.listdir(source_dir_path)
    except FileNotFoundError:
        print(f"Error: Source directory not found at {source_dir_path}")
        return

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item_name in dir_contents:
        source_item_path = os.path.join(source_dir_path, item_name)
        dest_item_path = os.path.join(dest_dir_path, item_name)

        if os.path.isfile(source_item_path):
            print(f"  Copying file: {source_item_path} to {dest_item_path}")
            shutil.copy(source_item_path, dest_item_path)

        elif os.path.isdir(source_item_path):
            print(f"  Creating directory: {dest_item_path}")
            copy_contents_recursive(source_item_path, dest_item_path)


def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()

    raise ValueError("Markdown must contain an H1 header (line starting with # )")

