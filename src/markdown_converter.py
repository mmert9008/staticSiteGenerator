from htmlnode import ParentNode, LeafNode
from textnode import text_to_textnodes, text_node_to_html_node, TextNode, TextType
from markdown_utils import markdown_to_blocks, block_to_block_type, BlockType


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children_html_nodes = []
    for text_node in text_nodes:
        children_html_nodes.append(text_node_to_html_node(text_node))
    return children_html_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_html_nodes = []

    if not blocks: # Handle empty or whitespace input based on test expectations
        # Return an empty div using LeafNode as ParentNode requires children
        return LeafNode("div", "")

    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = None

        if block_type == BlockType.PARAGRAPH:
            children = text_to_children(block)
            html_node = ParentNode("p", children)

        elif block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            heading_text = block[level:].strip()
            children = text_to_children(heading_text)
            html_node = ParentNode(f"h{level}", children)

        elif block_type == BlockType.CODE:
            # Code block special case: extract content and remove leading newline if present
            code_content = block[3:-3]
            if code_content.startswith('\n'):
                code_content = code_content[1:]
            raw_code_leaf = LeafNode(None, code_content)
            code_html = ParentNode("code", [raw_code_leaf])
            html_node = ParentNode("pre", [code_html])

        elif block_type == BlockType.QUOTE:
            lines = block.split('\n')
            processed_lines = [line[1:].strip() for line in lines] # Remove '>' and strip
            processed_text = "\n".join(processed_lines)
            children = text_to_children(processed_text)
            html_node = ParentNode("blockquote", children)

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split('\n')
            list_items = []
            for line in lines:
                item_text = line[2:]
                children = text_to_children(item_text)
                list_items.append(ParentNode("li", children))
            html_node = ParentNode("ul", list_items)

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split('\n')
            list_items = []
            for i, line in enumerate(lines):
                 dot_index = line.find('.')
                 space_index = line.find(' ', dot_index + 1)
                 item_text = line[space_index + 1:]
                 children = text_to_children(item_text)
                 list_items.append(ParentNode("li", children))
            html_node = ParentNode("ol", list_items)

        else:
            raise ValueError(f"Unknown block type: {block_type}")

        if html_node: # Only append if a node was created
            block_html_nodes.append(html_node)

    parent_div = ParentNode("div", block_html_nodes)
    return parent_div

