import re
from typing import Text
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
            raise Exception("This shouldn't happen")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            for i, text in enumerate(old_node.text.split(delimiter)):
                if not text:
                    continue
                if i % 2 == 0:
                    nodes.append(TextNode(text, TextType.TEXT))
                else:
                    nodes.append(TextNode(text, text_type))
        else:
            nodes.append(old_node)
    return nodes

def split_nodes_regex(old_nodes, prefix=""):
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            for i, text in enumerate(re.split(fr'(?<!!)({prefix}\[.+?\]\(.*?\))', old_node.text)):
                if not text:
                    continue
                if i % 2 == 0:
                    nodes.append(TextNode(text, TextType.TEXT))
                else:
                    if prefix:
                        items = extract_markdown_images(text)
                        nodes.append(TextNode(items[0][0], TextType.IMAGE, items[0][1]))
                    else:
                        items = extract_markdown_links(text)
                        nodes.append(TextNode(items[0][0], TextType.LINK, items[0][1]))
        else:
            nodes.append(old_node)
    return nodes

def split_nodes_image(old_nodes):
    return split_nodes_regex(old_nodes, "!")

def split_nodes_link(old_nodes):
    return split_nodes_regex(old_nodes)

def handle_link_img_regex(text, prefix=""):
    return re.findall(fr'(?:^| ){prefix}\[(.+?)\]\((.+?)\)', text)

def extract_markdown_images(text):
    return handle_link_img_regex(text, prefix="!")

def extract_markdown_links(text):
    return handle_link_img_regex(text)

def text_to_textnodes(text):
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD) 
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC) 
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = re.split(r'\s*\n\n+\s*', markdown.strip())
    return blocks


