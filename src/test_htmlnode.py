import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("h1", "Hello")
        self.assertEqual(repr(node), "HTMLNode(h1, Hello, None, None)")

    def test_props_to_html(self):
        node = HTMLNode("a", "test.url", props={"href": "http://test.url"})
        self.assertEqual(node.props_to_html(), ' href="http://test.url"')

    def test_to_html(self):
        node = HTMLNode("a", "test.url")
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_repr(self):
        node = LeafNode("h1", "Hello", {"href": "test.url"})
        self.assertEqual(repr(node), "HTMLNode(h1, Hello, None, {'href': 'test.url'})")

    def test_to_html(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()
        node1 = LeafNode(None, "test") # 
        self.assertEqual(node1.to_html(), "test")
        node2 = LeafNode("a", "test")
        self.assertEqual(node2.to_html(), "<a>test</a>")
        node3 = LeafNode("a", "test", {"href": "http://test.url"})
        self.assertEqual(node3.to_html(), "<a href=\"http://test.url\">test</a>")

    def test_to_html_props(self):
        node = LeafNode("a", "test.url", props={"href": "http://test.url"})
        self.assertEqual(node.props_to_html(), ' href="http://test.url"')


class TestParentNode(unittest.TestCase):
    def test_repr(self):
        test_node = LeafNode(None, "test")
        node = ParentNode("h1", [test_node])
        self.assertEqual(repr(node), "HTMLNode(h1, None, [HTMLNode(None, test, None, None)], None)")
    
    def test_to_html(self):
        node = LeafNode("b", "bold")
        node1 = ParentNode(None, ["test"]) # 
        with self.assertRaises(ValueError):
            node1.to_html()
        node2 = ParentNode("a", [node])
        self.assertEqual(node2.to_html(), "<a><b>bold</b></a>")
        node3 = ParentNode("a", [node, node2], {"href": "http://test.url"})
        self.assertEqual(node3.to_html(), '<a href="http://test.url"><b>bold</b><a><b>bold</b></a></a>')
        node = ParentNode("p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

if __name__ == "__main__":
    unittest.main(verbosity=2)
