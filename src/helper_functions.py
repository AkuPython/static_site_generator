from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise Exception("Invalid input, not a TextNode")
    if not text_node.text_type.name in [e.name for e in TextType]:
        raise Exception("Invalid TextNode.TextType")

    match text_node.text_type.name:
        case "TEXT":
            return LeafNode(None, text_node.text)
        case "BOLD":
            return LeafNode('b', text_node.text)
        case "ITALIC":
            return LeafNode('i', text_node.text)
        case "CODE":
            return LeafNode('code', text_node.text)
        case "LINK":
            return LeafNode('a', text_node.text, props={"href": text_node.url})
        case "IMAGE":
            return LeafNode('img', '', props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("This sholudn't happen")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    pass

