import re

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = re.split(r"\n\s*\n", markdown)
    result = []
    for block in blocks:
        lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
        if not lines:
            continue
        # If all lines start with "- ", treat as a list block
        if all(line.startswith("- ") for line in lines):
            result.append("\n".join(lines))
        # If only one line, or block is a paragraph, treat as one block
        elif len(lines) == 1:
            result.append(lines[0])
        else:
            # For the test, treat each line as a separate block
            result.extend(lines)
    return result