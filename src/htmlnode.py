class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        # Convert props dictionary to HTML attributes string
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        attrs = f" {props_html}" if props_html else ""
        return f"<{self.tag}{attrs}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children or [], props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        props_html = self.props_to_html()
        attrs = f" {props_html}" if props_html else ""
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{attrs}>{children_html}</{self.tag}>"
