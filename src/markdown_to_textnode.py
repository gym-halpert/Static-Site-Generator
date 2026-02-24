from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        parts = node.text.split(delimeter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown, unbalanced delimeter '{delimeter}' in '{node.text}'")

        for i, part in enumerate(parts):
            new_nodes.append(TextNode(part, TextType.TEXT if i % 2 == 0 else text_type))

    return new_nodes
