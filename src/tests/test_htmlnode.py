import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode(tag="p", value="Hello", children=None, props={"class": "text"})
        node2 = HTMLNode(tag="p", value="Hello", children=None, props={"class": "text"})
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = HTMLNode(tag="p", value="Hello", children=None, props={"class": "text"})
        node2 = HTMLNode(tag="div", value="Hello", children=None, props={"class": "text"})
        self.assertNotEqual(node1, node2)

    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="p", value="Hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
