import unittest

from main import text_node_to_html_node
from textnode import TextNode, TextType

class TestNodeConversion(unittest.TestCase):
  def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.to_html(), "This is a text node")
    
  def test_bold(self):
    node = TextNode("This is a bold node", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")
    
  def test_italic(self):
    node = TextNode("This is an italic node", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.to_html(), "<i>This is an italic node</i>")
    
  def test_code(self):
    node = TextNode("This is a code node", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")