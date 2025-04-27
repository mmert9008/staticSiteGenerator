import os
import shutil
import sys

from markdown_converter import markdown_to_html_node
from markdown_utils import extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.exists(from_path):
        print(f"Error: Markdown file not found at {from_path}")
        return

    if not os.path.exists(template_path):
        print(f"Error: Template file not found at {template_path}")
        return

    try:
        with open(from_path, 'r') as f:
            markdown_content = f.read()
    except Exception as e:
        print(f"Error reading markdown file {from_path}: {e}")
        return

    try:
        with open(template_path, 'r') as f:
            template_content = f.read()
    except Exception as e:
        print(f"Error reading template file {template_path}: {e}")
        return

    try:
        html_content = markdown_to_html_node(markdown_content).to_html()
    except ValueError as e:
        print(f"Error converting markdown to HTML for {from_path}: {e}")
        return

    try:
        page_title = extract_title(markdown_content)
    except ValueError as e:
        print(f"Error extracting title from {from_path}: {e}")
        return

    final_html = template_content.replace("{{ Title }}", page_title).replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir: # Check if dest_path includes a directory
        os.makedirs(dest_dir, exist_ok=True)

    try:
        with open(dest_path, 'w') as f:
            f.write(final_html)
    except Exception as e:
        print(f"Error writing final HTML file to {dest_path}: {e}")
        return

