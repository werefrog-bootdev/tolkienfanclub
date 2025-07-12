from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    def text_handler(node):
        return LeafNode(None, node.text)

    def bold_handler(node):
        return LeafNode("b", node.text)

    def italic_handler(node):
        return LeafNode("i", node.text)

    def code_handler(node):
        return LeafNode("code", node.text)

    def link_handler(node):
        if not node.url:
            raise ValueError("LINK TextNode must have a url")
        return LeafNode("a", node.text, {"href": node.url})

    def image_handler(node):
        if not node.url:
            raise ValueError("IMAGE TextNode must have a url")
        return LeafNode("img", "", {"src": node.url, "alt": node.text})

    handlers = {
        TextType.TEXT: text_handler,
        TextType.BOLD: bold_handler,
        TextType.ITALIC: italic_handler,
        TextType.CODE: code_handler,
        TextType.LINK: link_handler,
        TextType.IMAGE: image_handler,
    }

    handler = handlers.get(text_node.text_type)
    if not handler:
        raise Exception("Invalid TextType")
    return handler(text_node)


def main():
    node = TextNode("This is some anchor text", text_type=TextType.LINK, url="https://www.boot.dev")
    print(node)


if __name__ == '__main__':
    main()
