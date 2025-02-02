import unittest

import helper_functions
from htmlnode import LeafNode
from textnode import TextNode, TextType


class TestHelperFunctions(unittest.TestCase):
    def test_invalid(self):
        with self.assertRaises(Exception):
            helper_functions.text_node_to_html_node("a")
        with self.assertRaises(Exception):
            helper_functions.text_node_to_html_node(TextNode("test_text", "not_a_text_type"))

    def test_text(self):
        node = TextNode('test', TextType.TEXT)
        self.assertEqual(helper_functions.text_node_to_html_node(node), LeafNode(None, 'test'))

    def test_bold(self):
        node = TextNode('test', TextType.BOLD)
        self.assertEqual(helper_functions.text_node_to_html_node(node), LeafNode('b', 'test'))

    def test_italic(self):
        node = TextNode('test', TextType.ITALIC)
        self.assertEqual(helper_functions.text_node_to_html_node(node), LeafNode('i', 'test'))

    def test_code(self):
        node = TextNode('test', TextType.CODE)
        self.assertEqual(helper_functions.text_node_to_html_node(node), LeafNode('code', 'test'))

    def test_link(self):
        node = TextNode('test', TextType.LINK, "http://test.url")
        self.assertEqual(helper_functions.text_node_to_html_node(node), LeafNode('a', 'test', props={"href": "http://test.url"}))

    def test_image(self):
        node = TextNode('test', TextType.IMAGE, "http://test.url")
        self.assertEqual(helper_functions.text_node_to_html_node(node), LeafNode('img', '', props={'src': 'http://test.url', "alt": "test"}))
    
    def test_splitnodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = helper_functions.split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, 
                        [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                        ])

    def test_splitnodes_bigtest(self):
        node = TextNode("This is **bold text** with a `code block` word, and *some_italics*", TextType.TEXT)
        new_nodes1 = helper_functions.split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes2 = helper_functions.split_nodes_delimiter(new_nodes1, "**", TextType.BOLD)
        new_nodes3 = helper_functions.split_nodes_delimiter(new_nodes2, "*", TextType.ITALIC)
        self.assertEqual(new_nodes1,
                        [
                            TextNode("This is **bold text** with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word, and *some_italics*", TextType.TEXT),
                        ])
        self.assertEqual(new_nodes2,
                        [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("bold text", TextType.BOLD),
                            TextNode(" with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word, and *some_italics*", TextType.TEXT),
                        ])
        self.assertEqual(new_nodes3,
                        [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("bold text", TextType.BOLD),
                            TextNode(" with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word, and ", TextType.TEXT),
                            TextNode("some_italics", TextType.ITALIC),
                            TextNode("", TextType.TEXT),
                        ])
       
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text2 = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(helper_functions.extract_markdown_images(text), 
                         [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                          ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        self.assertEqual(helper_functions.extract_markdown_images(text2), [])

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        text2 = "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(helper_functions.extract_markdown_links(text), 
                         [("to boot dev", "https://www.boot.dev"),
                          ("to youtube", "https://www.youtube.com/@bootdotdev")])
        self.assertEqual(helper_functions.extract_markdown_links(text2), [])

if __name__ == "__main__":
    unittest.main()

