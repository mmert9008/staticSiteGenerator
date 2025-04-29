import os
import shutil
import sys

from markdown_utils import copy_contents_recursive
from page_generator import generate_pages_recursive


def main():
    print("Starting static site generation...")

    static_dir_path = "static"
    dest_dir_path = "docs"
    content_path = "content"
    template_path = "template.html"

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        if not basepath.endswith('/'):
             basepath += '/'


    if not os.path.exists(static_dir_path):
        print(f"Error: Static directory not found at {static_dir_path}")
        sys.exit(1)

    if os.path.exists(dest_dir_path):
        print(f"Cleaning destination directory: {dest_dir_path}")
        shutil.rmtree(dest_dir_path)

    print(f"Creating destination directory: {dest_dir_path}")
    os.mkdir(dest_dir_path)

    copy_contents_recursive(static_dir_path, dest_dir_path)

    generate_pages_recursive(content_path, template_path, dest_dir_path, basepath)

    print("Static site generation finished.")


if __name__ == "__main__":
    main()

