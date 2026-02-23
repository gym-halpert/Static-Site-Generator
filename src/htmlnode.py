class HTMLNode():

    def __init__(self = None, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        final_string = ""
        for k, v in self.props.items():
            k = k.strip('"')
            final_string += f'{k}="{v}" '
        return final_string.rstrip(" ")

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        if value is None:
            raise ValueError("Leaf must have a value.")
        super().__init__(tag, value, children = [], props = props)

    def to_html(self):
        if self.tag is None:
            return self.value
        return f'<{self.tag}>{self.value}</{self.tag}>'

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.props == other.props)

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
