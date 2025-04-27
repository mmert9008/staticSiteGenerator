import os
import shutil
import sys

from markdown_utils import copy_contents_recursive
from page_generator import generate_page


def main():
    print("Starting static site generation...")

    static_dir_path = "static"
    public_dir_path = "public"
    content_path = "content"
    template_path = "template.html" # Assuming template.html is in the root

    # Check if the static directory exists
    if not os.path.exists(static_dir_path):
        print(f"Error: Static directory not found at {static_dir_path}")
        sys.exit(1)

    # Clean destination directory if it exists
    if os.path.exists(public_dir_path):
        print(f"Cleaning destination directory: {public_dir_path}")
        shutil.rmtree(public_dir_path)

    # Create destination directory
    print(f"Creating destination directory: {public_dir_path}")
    os.mkdir(public_dir_path)

    # Copy static files from static to public
    copy_contents_recursive(static_dir_path, public_dir_path)

    # Generate the index page
    index_md_path = os.path.join(content_path, "index.md")
    index_html_path = os.path.join(public_dir_path, "index.html")
    generate_page(index_md_path, template_path, index_html_path)


    print("Static site generation finished.")


if __name__ == "__main__":
    main()

