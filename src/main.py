import re
from src.leafnode import LeafNode
from src.textnode import TextNode, TextType
from src.markdown_utils import extract_markdown_images, extract_markdown_links
from src.split_nodes import split_nodes_image, split_nodes_link, split_nodes_delimiter

def main():
  text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
  print(text_node)

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


if __name__ == "__main__":
  main()
