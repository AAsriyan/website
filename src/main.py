from leafnode import LeafNode
from textnode import TextNode, TextType
from blocknode import BlockType
from split_nodes import split_nodes_image, split_nodes_link, split_nodes_delimiter
from title_extractor import extract_title
import re
import os
import shutil

def copy_static_to_public(src_path="static", dest_path="public"):
    """
    Recursively copies all contents from source directory to destination directory.
    First deletes all contents of the destination directory to ensure a clean copy.
    """
    print(f"Starting copy from '{src_path}' to '{dest_path}'")
    
    # Delete destination directory if it exists
    if os.path.exists(dest_path):
        print(f"Removing existing '{dest_path}' directory")
        shutil.rmtree(dest_path)
    
    # Create destination directory
    print(f"Creating '{dest_path}' directory")
    os.mkdir(dest_path)
    
    # Check if source directory exists
    if not os.path.exists(src_path):
        print(f"Source directory '{src_path}' does not exist")
        return
    
    # Copy contents recursively
    _copy_directory_contents(src_path, dest_path)
    print(f"Finished copying from '{src_path}' to '{dest_path}'")

def _copy_directory_contents(src_dir, dest_dir):
    """
    Helper function to recursively copy directory contents.
    """
    # List all items in the source directory
    for item in os.listdir(src_dir):
        src_item_path = os.path.join(src_dir, item)
        dest_item_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(src_item_path):
            # It's a file, copy it
            print(f"Copying file: {src_item_path} -> {dest_item_path}")
            shutil.copy(src_item_path, dest_item_path)
        else:
            # It's a directory, create it and recursively copy its contents
            print(f"Creating directory: {dest_item_path}")
            os.mkdir(dest_item_path)
            _copy_directory_contents(src_item_path, dest_item_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages from all markdown files in a directory structure.
    
    Args:
        dir_path_content: Path to the content directory to crawl
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory where HTML files should be written
    """
    # Import here to avoid circular imports
    from markdown_html import markdown_to_html_node
    
    print(f"Crawling directory: {dir_path_content}")
    
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    
    # List all items in the content directory
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(item_path):
            # Check if it's a markdown file
            if item.endswith('.md'):
                # Generate HTML file with same name but .html extension
                html_filename = item.replace('.md', '.html')
                dest_file_path = os.path.join(dest_dir_path, html_filename)
                
                # Generate the page
                generate_page(item_path, template_path, dest_file_path)
        
        elif os.path.isdir(item_path):
            # It's a directory, create corresponding directory in destination and recurse
            dest_subdir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, dest_subdir_path)

def main():
  # Delete anything in the public directory and copy static files
  copy_static_to_public()
  
  # Generate pages recursively from all markdown files in content directory
  generate_pages_recursive("content", "template.html", "public")
  
  print("Site generation complete!")

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
  match text_node.type:
    case TextType.TEXT:
      return LeafNode(None, text_node.text)
    case TextType.BOLD:
      return LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return LeafNode("i", text_node.text)
    case TextType.CODE:
      return LeafNode("code", text_node.text)
    case TextType.LINK:
      return LeafNode("a", text_node.text, {"href": text_node.url})
    case TextType.IMAGE:
      return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    case _:
      raise Exception(f"Unsupported text type: {text_node.type}")
    
def text_to_textnodes(text: str) -> list[TextNode]:
  nodes = [TextNode(text, TextType.TEXT)]
  nodes = split_nodes_image(nodes)
  nodes = split_nodes_link(nodes)
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
  return nodes

def block_to_block_type(block: str) -> BlockType:
  lines = block.split('\n')
  # Check for heading: 1-6 # characters, followed by a space and text
  if re.match(r'^#{1,6} .+', block):
    return BlockType.HEADING
  elif block.startswith("- ") and all(line.startswith("- ") for line in lines):
    return BlockType.UNORDERED_LIST
  elif re.match(r'^\d+\. ', block) and all(re.match(r'^\d+\. ', line) for line in lines):
    return BlockType.ORDERED_LIST
  elif block.startswith("```") and block.endswith("```"):
    return BlockType.CODE
  elif block.startswith(">") and all(line.startswith(">") for line in lines):
    return BlockType.QUOTE
  else:
    return BlockType.PARAGRAPH
  
def generate_page(from_path: str, template_path: str, dest_path: str):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path: Path to the source markdown file
        template_path: Path to the HTML template file
        dest_path: Path where the generated HTML file should be written
    """
    # Import here to avoid circular imports
    from markdown_html import markdown_to_html_node
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the final HTML to the destination file
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == "__main__":
  main()
