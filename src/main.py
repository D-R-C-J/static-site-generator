from pages import copy_to_destination, generate_pages_recursive
from textnode import TextNode, TextType


def main():
    dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(dummy)
    copy_to_destination()
    generate_pages_recursive("content/", "template.html", "public/")

main()
