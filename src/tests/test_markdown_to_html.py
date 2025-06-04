import unittest
from markdown_html import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    
    def test_paragraphs(self):
        """Test markdown paragraphs with inline formatting"""
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        """Test code block without inline formatting"""
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_headings(self):
        """Test various heading levels"""
        md = """
# Heading 1

## Heading 2 with **bold** text

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b> text</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        self.assertEqual(html, expected)
    
    def test_unordered_list(self):
        """Test unordered list with inline formatting"""
        md = """
- First item with **bold** text
- Second item with _italic_ text
- Third item with `code` text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ul><li>First item with <b>bold</b> text</li><li>Second item with <i>italic</i> text</li><li>Third item with <code>code</code> text</li></ul></div>"
        self.assertEqual(html, expected)
    
    def test_ordered_list(self):
        """Test ordered list with inline formatting"""
        md = """
1. First numbered item
2. Second item with **bold**
3. Third item with _italic_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><ol><li>First numbered item</li><li>Second item with <b>bold</b></li><li>Third item with <i>italic</i></li></ol></div>"
        self.assertEqual(html, expected)
    
    def test_quote_block(self):
        """Test quote block with inline formatting"""
        md = """
> This is a quote with **bold** text
> and _italic_ text on multiple lines
> with `code` as well
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = "<div><blockquote>This is a quote with <b>bold</b> text\nand <i>italic</i> text on multiple lines\nwith <code>code</code> as well</blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_mixed_content(self):
        """Test document with mixed block types"""
        md = """
# Main Title

This is a paragraph with **bold** and _italic_ text.

## Subtitle

- List item one
- List item two

```
def hello():
    print("Hello, **world**!")
```

> This is a quote
> with multiple lines

1. Numbered item
2. Another numbered item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Check that it contains all the expected elements
        self.assertIn("<h1>Main Title</h1>", html)
        self.assertIn("<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>", html)
        self.assertIn("<h2>Subtitle</h2>", html)
        self.assertIn("<ul><li>List item one</li><li>List item two</li></ul>", html)
        self.assertIn('<pre><code>def hello():\n    print("Hello, **world**!")\n</code></pre>', html)
        self.assertIn("<blockquote>This is a quote\nwith multiple lines</blockquote>", html)
        self.assertIn("<ol><li>Numbered item</li><li>Another numbered item</li></ol>", html)
        self.assertTrue(html.startswith("<div>"))
        self.assertTrue(html.endswith("</div>"))
    
    def test_empty_markdown(self):
        """Test empty markdown input"""
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
    
    def test_single_paragraph(self):
        """Test single paragraph"""
        md = "Just a simple paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>Just a simple paragraph.</p></div>")
    
    def test_code_block_with_language(self):
        """Test code block with language specification"""
        md = """
```python
def greet(name):
    return f"Hello, {name}!"
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><pre><code>python\ndef greet(name):\n    return f"Hello, {name}!"\n</code></pre></div>'
        self.assertEqual(html, expected)
    
    def test_links_and_images(self):
        """Test paragraphs with links and images"""
        md = """
This paragraph has a [link](https://example.com) in it.

This one has an ![image](https://example.com/image.png) in it.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        self.assertIn('<a href="https://example.com">link</a>', html)
        self.assertIn('<img src="https://example.com/image.png" alt="image">', html)


if __name__ == "__main__":
    unittest.main() 