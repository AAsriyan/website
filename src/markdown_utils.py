import re

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def markdown_to_blocks(markdown: str) -> list[str]:
    """Split markdown into blocks based on double newlines"""
    if not markdown.strip():
        return []
    
    # Split on double newlines to get raw blocks
    raw_blocks = re.split(r"\n\s*\n", markdown.strip())
    result = []
    
    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue
        
        lines = block.splitlines()
        clean_lines = [line.strip() for line in lines if line.strip()]
        
        if not clean_lines:
            continue
            
        # Check if it's a code block (starts and ends with ```) - keep as one block
        if block.startswith("```") and block.endswith("```"):
            result.append(block)
        # Check if it's an unordered list (all lines start with "- ") - keep as one block
        elif all(line.startswith("- ") for line in clean_lines):
            result.append("\n".join(clean_lines))
        # Check if it's an ordered list (all lines start with number. ) - keep as one block
        elif all(re.match(r'^\d+\. ', line) for line in clean_lines):
            result.append("\n".join(clean_lines))
        # Check if it's a quote block (all lines start with ">") - keep as one block
        elif all(line.startswith(">") for line in clean_lines):
            result.append("\n".join(clean_lines))
        # For single line blocks
        elif len(clean_lines) == 1:
            result.append(clean_lines[0])
        else:
            # Check if we have mixed content (heading mixed with other content)
            has_heading = any(line.startswith("#") for line in clean_lines)
            if has_heading:
                # If there's a heading mixed with other content, split each line
                result.extend(clean_lines)
            else:
                # If it's all paragraph content, keep as one block
                result.append("\n".join(clean_lines))
    
    return result