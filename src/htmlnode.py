
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        assert isinstance(tag, (type(None), str))
        assert isinstance(value, (type(None), str))
        assert isinstance(children, (type(None), list))
        assert isinstance(props, (type(None), dict))
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Used in child types")

    def props_to_html(self):
        if not isinstance(self.props, dict):
            raise Exception("props not set")
        return " " + " ".join([f'{k}="{v}"' for k, v in self.props.items()])

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if self.__repr__() == other.__repr__():
            return True
        return False


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Must have a value")
        if self.tag == None:
            return self.value
        props_str = ""
        if self.props:
            props_str += self.props_to_html()
        return f"<{self.tag + props_str}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Must have a tag")
        if not self.children:
            raise ValueError("Must have children")
        html = ""
        for child in self.children:
            if isinstance(child, str):
                html += child
                continue
            html += child.to_html()
        props_str = ""
        if self.props:
            props_str += self.props_to_html()
        return f"<{self.tag + props_str}>{html}</{self.tag}>"


