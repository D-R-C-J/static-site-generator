from pages import copy_to_destination, generate_page
from textnode import TextNode, TextType


def main():
    dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(dummy)
    copy_to_destination()
    generate_page("content/index.md", "template.html", "public/index.html")

main()
