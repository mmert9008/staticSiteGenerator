import re
from enum import Enum
# Note: TextNode and TextType are imported inside the split functions below


class BlockType(Enum):
    """
    Represents the different types of Markdown blocks.
    """
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
    # Import moved inside function to avoid circular dependency at top level
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
    # Import moved inside function to avoid circular dependency at top level
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
    """
    Determines the block type of a single markdown block string.
    Assumes the block has already been stripped of leading/trailing whitespace.
    """
    lines = block.split('\n')

    # Check for quote block (every line starts with >)
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Check for unordered list (every line starts with - )
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for ordered list (every line starts with number. )
    is_ordered_list = True
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    # Check for heading (starts with 1-6 # followed by space, single line)
    if re.match(r"#{1,6} ", block) and len(lines) == 1:
        return BlockType.HEADING

    # Check for code block (starts and ends with ```)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # If none of the above, it's a paragraph
    return BlockType.PARAGRAPH

