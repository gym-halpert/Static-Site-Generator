import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()

