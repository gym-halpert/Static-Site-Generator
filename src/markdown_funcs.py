import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        parts = node.text.split(delimeter)
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
            if section[0] != "":
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
            if section[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original = sections[1]
        if original != "":
            new_nodes.append(TextNode(original, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.TEXT)
    nodes = [initial_node]
    result1 = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    result2 = split_nodes_delimiter(result1, "_", TextType.ITALIC)
    result3 = split_nodes_delimiter(result2, "`", TextType.CODE)
    result4 = split_nodes_image(result3)
    result5 = split_nodes_link(result4)
    return result5

def extract_markdown_images(text):
    pattern = r'!\[([^\]]+)\]\((https?://[^\s)]+)\)'
    matches = re.findall(pattern, text)
    return [(alt, url) for alt, url in matches]

def extract_markdown_links(text):
    pattern = r'\[([^\]]+)\]\((https?://[^\s)]+)\)'
    matches = re.findall(pattern, text)
    return [(description, url) for description, url in matches]

def markdown_to_blocks(markdown):
    blocks = []
    markdown.split("\n\n")
    for block in markdown:
        stripped = block.strip()
        blocks.append(block)
    return blocks
