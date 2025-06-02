from src.htmlnode import HTMLNode

class LeafNode(HTMLNode):
  def __init__(self, tag: str, value: str, props: dict = None):
    super().__init__(tag, value, [], props)

  def to_html(self) -> str:
    if self.value is None:
      raise ValueError("value is required")
    
    if self.tag is None:
      return self.value
    
    if self.props is None:
      return f"<{self.tag}>{self.value}</{self.tag}>"
    
    props_str = ""
    for key, value in self.props.items():
      props_str += f'{key}="{value}"'
    
    return f"<{self.tag} {props_str.strip()}>{self.value}</{self.tag}>"
  
  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value}, {self.props})"
  
  def __eq__(self, other):
    return super().__eq__(other) and self.value == other.value and self.props == other.props