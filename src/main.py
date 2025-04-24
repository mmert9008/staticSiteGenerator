#!/usr/bin/env python3

from textnode import TextNode, TextType

def main():
    # Create a dummy TextNode object
    dummy_node = TextNode("This is some test text.", TextType.TEXT, None)
    print(dummy_node)

    # Create a link node example
    link_node = TextNode("Google", TextType.LINK, "https://www.google.com")
    print(link_node)

    # Create an image node example
    image_node = TextNode("Python Logo", TextType.IMAGE, "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png")
    print(image_node)

if __name__ == "__main__":
    main()

