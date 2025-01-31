
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not isinstance(self.props, dict):
            raise Exception("props not set")
        return " " + " ".join([f'{k}="{v}"' for k, v in self.props.items()])

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("Must have a value")
        if self.tag == None:
            return self.value
        props_str = ""
        if self.props:
            props_str += self.props_to_html()
        return f"<{self.tag + props_str}>{self.value}</{self.tag}>"

