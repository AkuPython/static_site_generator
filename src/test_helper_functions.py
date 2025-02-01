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

if __name__ == "__main__":
    unittest.main()

