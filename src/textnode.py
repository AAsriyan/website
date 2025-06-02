from enum import Enum

class TextType(Enum):
  TEXT = "text"
  BOLD = "bold"
  ITALIC = "italic"
  CODE = "code"
  LINK = "link"
  IMAGE = "image"
  
class TextNode:
  def __init__(self, text: str, text_type: TextType, url: str = None):
    self.text = text
    self.type = text_type
    self.url = url

  def __repr__(self):
    return f"TextNode({self.text}, {self.type.value}, {self.url})"

  def __eq__(self, other):
    return self.text == other.text and self.type == other.type and self.url == other.url