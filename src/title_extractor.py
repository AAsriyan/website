import re

def extract_title(markdown: str) -> str:
    """
    Extract the h1 header from markdown text.
    
    Args:
        markdown: The markdown text to extract the title from
        
    Returns:
        The title text without the # prefix and whitespace
        
    Raises:
        Exception: If no h1 header is found
    """
    lines = markdown.split('\n')
    
    for line in lines:
        # Check if line starts with exactly one # followed by a space
        if re.match(r'^# .+', line):
            # Extract title by removing the # and any leading/trailing whitespace
            title = line[1:].strip()
            return title
    
    # If we get here, no h1 header was found
    raise Exception("No h1 header found in markdown") 