class HTMLNode:
  def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
    
  def to_html(self) -> str:
    raise NotImplementedError("to_html is not implemented")

  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

  def __eq__(self, other):
    return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props