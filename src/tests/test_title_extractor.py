import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from title_extractor import extract_title

class TestExtractTitle(unittest.TestCase):
    
    def test_simple_h1(self):
        """Test extracting a simple h1 header"""
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")
    
    def test_h1_with_extra_whitespace(self):
        """Test h1 with extra whitespace"""
        markdown = "#   Hello World   "
        result = extract_title(markdown)
        self.assertEqual(result, "Hello World")
    
    def test_h1_with_multiple_lines(self):
        """Test h1 in markdown with multiple lines"""
        markdown = """Some intro text

# My Title

Some body content"""
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")
    
    def test_h1_with_inline_formatting(self):
        """Test h1 with inline markdown formatting"""
        markdown = "# **Bold** and *italic* title"
        result = extract_title(markdown)
        self.assertEqual(result, "**Bold** and *italic* title")
    
    def test_h1_first_line(self):
        """Test h1 as the first line"""
        markdown = """# First Line Title
        
Some content below"""
        result = extract_title(markdown)
        self.assertEqual(result, "First Line Title")
    
    def test_no_h1_header_raises_exception(self):
        """Test that missing h1 header raises an exception"""
        markdown = """## This is h2
        
### This is h3

Some paragraph text"""
        
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        
        self.assertEqual(str(context.exception), "No h1 header found in markdown")
    
    def test_empty_markdown_raises_exception(self):
        """Test that empty markdown raises an exception"""
        markdown = ""
        
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_only_whitespace_raises_exception(self):
        """Test that markdown with only whitespace raises an exception"""
        markdown = "   \n\n   \n"
        
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_h1_without_space_ignored(self):
        """Test that # without space is not considered h1"""
        markdown = """#NoSpace
        
## Real header but not h1"""
        
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_multiple_h1_returns_first(self):
        """Test that multiple h1 headers returns the first one"""
        markdown = """# First Title
        
Some content

# Second Title"""
        result = extract_title(markdown)
        self.assertEqual(result, "First Title")

if __name__ == '__main__':
    unittest.main() 