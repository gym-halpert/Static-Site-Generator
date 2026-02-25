import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdown_funcs import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a textnode", TextType.BOLD)
        node2 = TextNode("This is a textnode", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node3 = TextNode(24, TextType.BOLD)
        node4 = TextNode("This is another node", TextType.ITALIC)
        self.assertNotEqual(node3, node4)

    def test_type_not_eq(self):
        node5 = TextNode("This is a test node", TextType.BOLD)
        node6 = TextNode("This is another node", TextType.ITALIC)
        self.assertNotEqual(node5, node6)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()
