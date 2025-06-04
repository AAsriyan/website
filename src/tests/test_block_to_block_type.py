import unittest
from main import block_to_block_type
from blocknode import BlockType


class TestBlockToBlockType(unittest.TestCase):
    
    def test_heading_single_hash(self):
        """Test heading with single # character"""
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_multiple_hashes(self):
        """Test headings with 2-6 # characters"""
        test_cases = [
            "## This is a heading 2",
            "### This is a heading 3", 
            "#### This is a heading 4",
            "##### This is a heading 5",
            "###### This is a heading 6"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_requires_space(self):
        """Test that headings require a space after # characters"""
        invalid_headings = [
            "#No space after hash",
            "##No space after hashes",
            "###No space",
            "######No space after six hashes"
        ]
        for block in invalid_headings:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading_max_six_hashes(self):
        """Test that more than 6 # characters is not a heading"""
        block = "####### This should be a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list_single_line(self):
        """Test unordered list with single line"""
        block = "- This is a list item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_multiple_lines(self):
        """Test unordered list with multiple lines"""
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_invalid_mixed_lines(self):
        """Test that mixed line formats don't qualify as unordered list"""
        block = "- First item\nNot a list item\n- Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_single_line(self):
        """Test ordered list with single line"""
        block = "1. This is a numbered item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_multiple_lines(self):
        """Test ordered list with multiple lines"""
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_various_numbers(self):
        """Test ordered list with different starting numbers"""
        test_cases = [
            "10. Tenth item",
            "42. Forty-second item",
            "100. One hundredth item"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_invalid_mixed_lines(self):
        """Test that mixed line formats don't qualify as ordered list"""
        block = "1. First item\nNot a list item\n2. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_block_basic(self):
        """Test basic code block with backticks"""
        block = "```\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_with_language(self):
        """Test code block with language specification"""
        block = "```python\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_single_line(self):
        """Test single line code block"""
        block = "```print('Hello')```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote_single_line(self):
        """Test quote with single line"""
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_multiple_lines(self):
        """Test quote with multiple lines"""
        block = "> This is the first line of a quote\n> This is the second line\n> This is the third line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_invalid_mixed_lines(self):
        """Test that mixed line formats don't qualify as quote"""
        block = "> This is a quote\nThis is not a quote\n> This is a quote again"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_plain_text(self):
        """Test plain text is classified as paragraph"""
        block = "This is just a plain paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_multiple_lines(self):
        """Test multi-line text is classified as paragraph"""
        block = "This is the first line.\nThis is the second line.\nThis is the third line."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_invalid_formats(self):
        """Test various invalid formats that should default to paragraph"""
        test_cases = [
            "#No space after hash",
            "-Missing space after dash",
            "1.Missing space after number",
            "```incomplete code block",
            "> Incomplete quote\nMissing quote marker"
        ]
        for block in test_cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_empty_string(self):
        """Test empty string defaults to paragraph"""
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_whitespace_only(self):
        """Test whitespace-only string defaults to paragraph"""
        block = "   \n  \t  \n   "
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main() 