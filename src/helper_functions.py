import os
from os.path import isfile
import re
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode

from enum import Enum

class BlockType(Enum):
    paragraph = "Paragraph"
    heading = "Heading"
    code = "Code"
    quote = "Quote"
    unordered_list = "Unordered_list"
    ordered_list = "Ordered_list"
    image = "Image"


class BlockNode:
    def __init__(self, text, block_type, level=None):
        self.text = text
        self.block_type = block_type
        self.level = level

    def __repr__(self):
        return f"BlockNode({self.text}, {self.block_type.value}, {self.level})"

    def __eq__(self, other):
        if self.__repr__() == other.__repr__():
            return True
        return False

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
                    if text_type == TextType.CODE:
                        text = text.strip()
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
    #nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC) 
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC) 
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = re.split(r'\s*\n\n+\s*', markdown.strip())
    return blocks

def block_to_block_type(block):
    def check_type(cur_block_type, prev_block_type):
        if prev_block_type in (None, cur_block_type):
            return True
        return False
    block_type = None
    start = None
    lines = block.split('\n')
    if block.startswith("`") and block.endswith("`"):
        lines = []
        block_type = BlockType.code
    if len(lines) == 1 and (match := re.match(r'(^#+)(?: )', lines[0])):
        return BlockNode(lines[0][match.end():], BlockType.heading, level=len(match.group(1)))
    for line in lines:
        if line[0] == '>' and check_type(BlockType.quote, block_type):
            block_type = BlockType.quote
        elif line[:2] in ("* ", "- ") and check_type(BlockType.unordered_list, block_type):
            block_type = BlockType.unordered_list
        elif (s := re.match(r'^(\d+)\. ', line)) and check_type(BlockType.ordered_list, block_type):
            if start == None:
                start = 0
            if int(s.groups()[0]) == start + 1:
                start += 1
                block_type = BlockType.ordered_list
            else:
                start = None
                block_type = BlockType.paragraph
        else:
            block_type = BlockType.paragraph
            break
    return BlockNode(block, block_type, level=start)

def text_to_children(text, tag):
    nodes = text_to_textnodes(text)
    htmlnodes = []
    for node in nodes:
         htmlnodes.append(text_node_to_html_node(node))
    if len(htmlnodes) == 1:
        htmlnodes[0].tag = tag
        return htmlnodes[0]
    return ParentNode(tag, htmlnodes)

def markdown_to_html_node(markdown):
    html_nodes = []
    for markdown_block in markdown_to_blocks(markdown):
        markdown_node = block_to_block_type(markdown_block)
        match markdown_node.block_type:
            case markdown_node.block_type.heading:
                html_nodes.append(text_to_children(markdown_node.text, f"h{markdown_node.level}"))
            case markdown_node.block_type.paragraph:
                if re.match(r'^!?\[.+?\]\(.+?\)$', markdown_node.text.strip()):
                    tn = text_to_textnodes(markdown_node.text)
                    html_nodes.append(text_node_to_html_node(tn[0]))
                else:
                    html_nodes.append(text_to_children(markdown_node.text, "p"))
            case markdown_node.block_type.unordered_list:
                li = lambda txt: text_to_children(txt[2:], 'li')
                ul = ParentNode('ul', list(map(li, markdown_node.text.split('\n'))))
                html_nodes.append(ul)
            case markdown_node.block_type.ordered_list:
                li = lambda txt: text_to_children(txt[txt.find(" ") + 1:], 'li')
                ol = ParentNode('ol', list(map(li, markdown_node.text.split('\n'))))
                html_nodes.append(ol)
            case markdown_node.block_type.code:
                html_nodes.append(text_to_children(markdown_node.text, "code"))
            case markdown_node.block_type.quote:
                text = '\n'.join([ i[(2 if i.startswith('> ') else 1):] for i in markdown_node.text.split('\n') ])
                html_nodes.append(text_to_children(text, "blockquote"))
            case _:
                print('what is this', markdown_node.block_type)
    return ParentNode('div', html_nodes)

def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("No H1 header Found")

def make_content_subfolders(file):
    dirs = file[:file.rfind("/")]
    if not os.path.exists(dirs):
        os.makedirs(dirs)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as fh:
        markdown = ''.join(fh.readlines())
    with open(template_path) as fh:
        template = ''.join(fh.readlines())
    outfile = template.replace("{{ Title }}", extract_title(markdown))
    outfile = outfile.replace("{{ Content }}", markdown_to_html_node(markdown).to_html())
    make_content_subfolders(dest_path)
    with open(dest_path, 'w+') as fh:
        fh.write(outfile)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        current = f'{dir_path_content}/{item}'
        dest = f'{dest_dir_path}/{item}'
        if os.path.isfile(current):
            print(current, template_path, dest_dir_path)
            generate_page(current, template_path, dest.replace('.md', '.html'))
        else:
            print(current, template_path, dest)
            generate_pages_recursive(current, template_path, dest)

