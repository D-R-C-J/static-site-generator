import sys

from pages import copy_to_destination, generate_pages_recursive
from textnode import TextNode, TextType


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_to_destination()
    generate_pages_recursive("content/", "template.html", "docs/", basepath)

main()
