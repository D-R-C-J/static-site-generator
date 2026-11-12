from enum import Enum
import re
from htmlnode import HTMLNode, ParentNode
from splitdelimiter import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "multiline code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks_list = markdown.split(sep="\n\n")
    filtered_list = [x.strip() for x in blocks_list if x.strip() != ""]
    return filtered_list

def block_to_block_type(markdown_block:str) -> BlockType:
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "######")):
        return BlockType.HEADING
    if markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE
    lines = markdown_block.splitlines()
    if lines and all(line.startswith((">")) for line in lines):
        return BlockType.QUOTE
    if lines and all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if lines and all(re.match(r"^\d+\.\s", line) for line in lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text:str) -> list[HTMLNode]:
    txt_nodes = text_to_textnodes(text)
    html_nodes = []
    for k in range(len(txt_nodes)):
        html_nodes.append(text_node_to_html_node(txt_nodes[k]))
    return html_nodes

def paragraph_to_html_node(block):
    lines = block.splitlines()
    children = text_to_children(" ".join(lines))
    return ParentNode("p", children, None)

def heading_to_html_node(block):
    lines = block.splitlines()
    count = len(lines[0]) - len(lines[0].lstrip("#"))
    tag = f"h{count}"
    lines[0] = lines[0][count:].strip()
    children = text_to_children(" ".join(lines))
    return ParentNode(tag, children, None)

def code_to_html_node(block):
    lines = block.splitlines()
    lines.pop(0)
    lines.pop(-1)
    code_text = "\n".join(lines) + "\n"
    txt_node = TextNode(code_text, TextType.TEXT)
    html_child = text_node_to_html_node(txt_node)
    code_node = ParentNode("code", [html_child])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.splitlines()
    for i in range(len(lines)):
        lines[i] = lines[i][1:].strip()
    children = text_to_children(" ".join(lines))
    return ParentNode("blockquote", children, None)


def ulist_to_html_node(block):
    lines = block.splitlines()
    li = []
    for i in range(len(lines)):
        lines[i] = lines[i][1:].strip()
        li.append(ParentNode("li", text_to_children(lines[i])))
    return ParentNode("ul", li, None)


def olist_to_html_node(block):
    lines = block.splitlines()
    li = []
    for i in range(len(lines)):
        lines[i] = re.sub(r"^\d+\.\s", "", lines[i]).strip()
        li.append(ParentNode("li", text_to_children(lines[i])))
    return ParentNode("ol", li, None)

def block_to_html_node(block):
    if block_to_block_type(block) == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_to_block_type(block) == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_to_block_type(block) == BlockType.CODE:
        return code_to_html_node(block)
    if block_to_block_type(block) == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_to_block_type(block) == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_to_block_type(block) == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode("div", [])
    for block in blocks:
        parent.children.append(block_to_html_node(block))
    return parent


    
