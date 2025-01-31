import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("h1", "Hello")
        self.assertEqual(repr(node), "HTMLNode(h1, Hello, None, None)")

    def test_props_to_html(self):
        node = HTMLNode("a", "test.url", props={"href": "http://test.url"})
        self.assertEqual(node.props_to_html(), ' href="http://test.url"')

    def to_html(self):
        node = HTMLNode("a", "test.url")
        self.assertEqual(node.to_html(), NotImplemented)


class TestLeafNode(unittest.TestCase):
    def test_repr(self):
        node = LeafNode("h1", "Hello", {"href": "test.url"})
        self.assertEqual(repr(node), "HTMLNode(h1, Hello, None, {'href': 'test.url'})")

    def test_to_html(self):
        # node = LeafNode("a", None)
        # self.assertRaises(node.to_html(), ValueError)
        node1 = LeafNode(None, "test") # 
        self.assertEqual(node1.to_html(), "test")
        node2 = LeafNode("a", "test")
        self.assertEqual(node2.to_html(), "<a>test</a>")
        node3 = LeafNode("a", "test", {"href": "http://test.url"})
        self.assertEqual(node3.to_html(), "<a href=\"http://test.url\">test</a>")

    def test_to_html_props(self):
        node = LeafNode("a", "test.url", props={"href": "http://test.url"})
        self.assertEqual(node.props_to_html(), ' href="http://test.url"')

    

if __name__ == "__main__":
    unittest.main()
