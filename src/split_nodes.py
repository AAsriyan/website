from src.textnode import TextNode, TextType
from src.markdown_utils import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def _split_nodes_by_extractor(old_nodes, extractor, node_type):
    new_nodes = []
    for node in old_nodes:
        if node.type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        matches = extractor(text)
        if not matches:
            new_nodes.append(node)
            continue
        curr_idx = 0
        for label, url in matches:
            if node_type == TextType.IMAGE:
                md = f"![{label}]({url})"
            else:
                md = f"[{label}]({url})"
            idx = text.find(md, curr_idx)
            if idx == -1:
                continue
            before = text[curr_idx:idx]
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(label, node_type, url))
            curr_idx = idx + len(md)
        after = text[curr_idx:]
        if after:
            new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    return _split_nodes_by_extractor(old_nodes, extract_markdown_images, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return _split_nodes_by_extractor(old_nodes, extract_markdown_links, TextType.LINK)