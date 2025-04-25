class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""

        html_attributes = []
        for key, value in self.props.items():
            html_attributes.append(f' {key}="{value}"')

        return "".join(html_attributes)

    def __repr__(self):
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        if self.value is None:
            raise ValueError("Leaf nodes require a value")

    def to_html(self):
        if self.tag is None:
            return self.value

        props_string = self.props_to_html()

        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag='{self.tag}', value='{self.value}', props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

        if self.tag is None:
            raise ValueError("ParentNode requires a tag")
        if self.children is None or len(self.children) == 0:
             raise ValueError("ParentNode requires children")


    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode requires a tag")
        if self.children is None or len(self.children) == 0:
             raise ValueError("ParentNode requires children")

        props_string = self.props_to_html()

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{props_string}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag='{self.tag}', children={self.children}, props={self.props})"

