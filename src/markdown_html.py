from main import block_to_block_type, text_to_textnodes, text_node_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode
from htmlnode import HTMLNode
from markdown_utils import markdown_to_blocks
from blocknode import BlockType
import re

class EmptyDivNode(HTMLNode):
    """A special node for empty div tags"""
    def __init__(self):
        super().__init__("div", "", [], None)
    
    def to_html(self) -> str:
        return "<div></div>"

def text_to_children(text: str) -> list:
    """Convert text with inline markdown to list of HTMLNode children"""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def heading_to_html_node(block: str) -> ParentNode:
    """Convert heading block to HTMLNode"""
    # Count the number of # characters
    hash_count = 0
    for char in block:
        if char == '#':
            hash_count += 1
        else:
            break
    
    # Extract heading text (remove # and space)
    heading_text = block[hash_count:].strip()
    
    # Create heading tag (h1-h6)
    tag = f"h{hash_count}"
    children = text_to_children(heading_text)
    
    return ParentNode(tag, children)

def paragraph_to_html_node(block: str) -> ParentNode:
    """Convert paragraph block to HTMLNode"""
    # Remove newlines and replace with spaces for inline text
    text = block.replace('\n', ' ')
    children = text_to_children(text)
    return ParentNode("p", children)

def code_block_to_html_node(block: str) -> ParentNode:
    """Convert code block to HTMLNode"""
    # Remove the ``` markers and get inner content
    # Strip only leading newline but preserve trailing content as-is
    code_content = block[3:-3]
    if code_content.startswith('\n'):
        code_content = code_content[1:]
    
    # For code blocks, we don't parse inline markdown
    code_node = LeafNode("code", code_content)
    return ParentNode("pre", [code_node])

def quote_to_html_node(block: str) -> ParentNode:
    """Convert quote block to HTMLNode"""
    lines = block.split('\n')
    # Remove '> ' from each line, handling both '> ' and '>' cases
    quote_lines = []
    for line in lines:
        if line.startswith('> '):
            quote_lines.append(line[2:])
        elif line.startswith('>'):
            quote_lines.append(line[1:])
        else:
            quote_lines.append(line)
    
    quote_text = '\n'.join(quote_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block: str) -> ParentNode:
    """Convert unordered list block to HTMLNode"""
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        if line.startswith('- '):
            # Remove '- ' from beginning
            item_text = line[2:]
            item_children = text_to_children(item_text)
            list_items.append(ParentNode("li", item_children))
    
    return ParentNode("ul", list_items)

def ordered_list_to_html_node(block: str) -> ParentNode:
    """Convert ordered list block to HTMLNode"""
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Remove number and '. ' from beginning
        match = re.match(r'^\d+\. ', line)
        if match:
            item_text = line[match.end():]
            item_children = text_to_children(item_text)
            list_items.append(ParentNode("li", item_children))
    
    return ParentNode("ol", list_items)

def markdown_to_html_node(markdown: str) -> HTMLNode:
    """Convert full markdown document to single parent HTMLNode"""
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.HEADING:
            html_node = heading_to_html_node(block)
        elif block_type == BlockType.PARAGRAPH:
            html_node = paragraph_to_html_node(block)
        elif block_type == BlockType.CODE:
            html_node = code_block_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            html_node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            html_node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            html_node = ordered_list_to_html_node(block)
        else:
            # Default to paragraph for unknown types
            html_node = paragraph_to_html_node(block)
        
        children.append(html_node)
    
    # Handle empty markdown case - return empty div
    if not children:
        return EmptyDivNode()
    
    # Return parent div containing all blocks
    return ParentNode("div", children)

def markdown_to_html(markdown: str) -> ParentNode:
    """Legacy function - use markdown_to_html_node instead"""
    return markdown_to_html_node(markdown)