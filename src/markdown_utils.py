import re
from textnode import TextNode, TextType


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
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

