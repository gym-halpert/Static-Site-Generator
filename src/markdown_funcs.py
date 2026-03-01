import re
from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown, unbalanced delimiter '{delimiter}' in '{node.text}'")
        for i, part in enumerate(parts):
            new_nodes.append(TextNode(part, TextType.TEXT if i % 2 == 0 else text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original = node.text
        images = extract_markdown_images(original)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = original.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original = sections[1]
        if original != "":
            new_nodes.append(TextNode(original, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original = node.text
        links = extract_markdown_links(original)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = original.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original = sections[1]
        if original != "":
            new_nodes.append(TextNode(original, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.TEXT)
    nodes = [initial_node]
    result1 = split_nodes_image(nodes)
    result2 = split_nodes_link(result1)
    result3 = split_nodes_delimiter(result2, "**", TextType.BOLD)
    result4 = split_nodes_delimiter(result3, "_", TextType.ITALIC)
    result5 = split_nodes_delimiter(result4, "`", TextType.CODE)
    return result5

def extract_markdown_images(text):
    pattern = r'!\[([^\]]+)\]\(([^\s)]+)\)'
    matches = re.findall(pattern, text)
    return [(alt, url) for alt, url in matches]

def extract_markdown_links(text):
    pattern = r'\[([^\]]+)\]\(([^\s)]+)\)'
    matches = re.findall(pattern, text)
    return [(description, url) for description, url in matches]

def markdown_to_blocks(markdown):
    blocks = []
    split_blocks = markdown.split("\n\n")
    for block in split_blocks:
        stripped = block.strip()
        blocks.append(stripped)
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    heading_pattern = r'^(#{1,6})\s+(.+)'
    code_pattern = r'(^```[\r\n]+)(.*?)(^```)'
    quote_pattern = r'(^>\s?.*\n?)+'
    unordered_list_pattern = r'(^-\s.*(\n|$))+'
    ordered_list_pattern = r'^(?P<number>[1-9]\d*.)\s.+(\n|$)'

    if re.match(heading_pattern, block):
        return BlockType.HEADING
    elif re.match(code_pattern, block):
        return BlockType.CODE
    elif re.match(quote_pattern, block):
        return BlockType.QUOTE
    elif re.match(unordered_list_pattern, block):
        return BlockType.UNORDERED_LIST
    elif re.match(ordered_list_pattern, block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

if __name__ == "__main__":
    test_text = "[Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)"
    print(f"Testing: {test_text}")
    print(f"Result: {extract_markdown_links(test_text)}")
