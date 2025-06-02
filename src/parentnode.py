from src.htmlnode import HTMLNode

class ParentNode(HTMLNode):
  def __init__(self, tag: str, children: list, props: dict = None):
    super().__init__(tag, None, children, props)

  def to_html(self) -> str:
    if self.tag is None:
      raise ValueError("tag is required")
    
    if bool(self.children) == False:
      raise ValueError("children is required")
    
    children_str = ""
    for child in self.children:
      children_str += child.to_html()
      
    if self.props is None:
      return f"<{self.tag}>{children_str}</{self.tag}>"
    
    props_str = ""
    for key, value in self.props.items():
      props_str += f'{key}="{value}"'
    
    return f"<{self.tag} {props_str.strip()}>{children_str}</{self.tag}>"