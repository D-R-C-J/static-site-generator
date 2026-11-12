import unittest
from splitdelimiter import *
from textnode import *

class TestSplitDelimiter(unittest.TestCase):
    def test_function(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        results = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, results)
    def test_multiple_bold(self):
        node = TextNode("This has **two** bold **words** here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertTrue(new_nodes[1].text_type == new_nodes[3].text_type == TextType.BOLD)
    def test_unclosed_delimiter(self):
        node = TextNode("This has `broken code", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    def test_extract_markdown_images(self):
                matches = extract_markdown_images(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
                )
                self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)      
    def test_split_images(self):
          node = TextNode(
              "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
              TextType.TEXT,
          )
          new_nodes = split_nodes_image([node])
          self.assertListEqual(
              [
                  TextNode("This is text with an ", TextType.TEXT),
                  TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                  TextNode(" and another ", TextType.TEXT),
                  TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
              ],
              new_nodes,
          )
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node = text_to_textnodes(text)
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(node, result)
