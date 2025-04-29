import os
import shutil
import sys

from markdown_utils import copy_contents_recursive
from page_generator import generate_pages_recursive


def main():
    print("Starting static site generation...")

    static_dir_path = "static"
    public_dir_path = "public"
    content_path = "content"
    template_path = "template.html"

    if not os.path.exists(static_dir_path):
        print(f"Error: Static directory not found at {static_dir_path}")
        sys.exit(1)

    if os.path.exists(public_dir_path):
        print(f"Cleaning destination directory: {public_dir_path}")
        shutil.rmtree(public_dir_path)

    print(f"Creating destination directory: {public_dir_path}")
    os.mkdir(public_dir_path)

    copy_contents_recursive(static_dir_path, public_dir_path)

    generate_pages_recursive(content_path, template_path, public_dir_path)


    print("Static site generation finished.")


if __name__ == "__main__":
    main()

