import unittest

from htmlnode import HTMLNode, LeafNode

children = ["These", "are", "children"]
props = {"href": "https://www.boot.dev", "target": "_blank"}

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("This is a tag", "This is a value", children, props)
        node2 = HTMLNode("This is a tag", "This is a value", children, props)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node3 = HTMLNode("This is a tag", "This is a value", children, props)
        node4 = HTMLNode("This is a value", "This is a tag", props, children)
        self.assertNotEqual(node3, node4)

    def test_leaf_to_html(self):
        node5 = LeafNode("p", "Hello world!")
        self.assertEqual(node5.to_html(), "<p>Hello world!</p>")

    def test_leaf_not_html(self):
        node6 = LeafNode("a", children)
        self.assertNotEqual(node6.to_html(), "<a>These are children</a")

if __name__ == "__main__":
    unittest.main()

