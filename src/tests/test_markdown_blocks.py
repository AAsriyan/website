import unittest
from src.markdown_utils import markdown_to_blocks

class TestMarkdownBlocks(unittest.TestCase):
  def test_markdown_to_blocks(self):
    markdown = """
    # Hello
    This is a test
    """
    blocks = markdown_to_blocks(markdown)
    self.assertEqual(blocks, ["# Hello", "This is a test"])
  
def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
				blocks,
				[
						"This is **bolded** paragraph",
						"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
						"- This is a list\n- with items",
				],
		)