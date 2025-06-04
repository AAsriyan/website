import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
  def test_leaf_to_html_p_with_props(self):
    node = LeafNode("p", "Hello, world!", {"class": "text"})
    self.assertEqual(node.to_html(), "<p class=\"text\">Hello, world!</p>")
    
  def test_leaf_to_html_p_with_children(self):
    node = LeafNode("p", "Hello, world!", {"id": "text"})
    self.assertEqual(node.to_html(), "<p id=\"text\">Hello, world!</p>")

if __name__ == "__main__":
  unittest.main()