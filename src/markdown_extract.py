import re

from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from markdown_inline_parser import text_to_textnodes


def extract_markdown_images(text):
    # Matches ![alt](url)
    return re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", text)


def extract_markdown_links(text):
    # Matches [text](url) but not images
    return re.findall(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)", text)


def text_node_to_html_node(textnode: TextNode) -> LeafNode:
    """
    Convert a TextNode to a corresponding LeafNode using a functional dispatch table.
    """
    def span(tn): return LeafNode(None, tn.text)
    def bold(tn): return LeafNode("b", tn.text)
    def italic(tn): return LeafNode("i", tn.text)
    def code(tn): return LeafNode("code", tn.text)
    def link(tn): return LeafNode("a", tn.text, {"href": tn.url})
    def image(tn): return LeafNode("img", "", {"src": tn.url, "alt": tn.text})

    dispatch = {
        TextType.TEXT: span,
        TextType.BOLD: bold,
        TextType.ITALIC: italic,
        TextType.CODE: code,
        TextType.LINK: link,
        TextType.IMAGE: image,
    }

    try:
        return dispatch[textnode.text_type](textnode)
    except KeyError:
        raise ValueError(f"Unknown TextType: {textnode.text_type}")


def text_to_children(text: str) -> list[LeafNode | ParentNode]:
    """
    Convert a string of markdown inline content to a list of HTMLNodes.
    """
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in textnodes]


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Convert a full markdown document to a single root HTML <div> node
    containing all child block elements.
    """
    def join_lines(block: str) -> str:
        return " ".join(line.strip() for line in block.splitlines())

    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.PARAGRAPH:
            clean_text = join_lines(block)
            children.append(ParentNode("p", text_to_children(clean_text)))

        elif btype == BlockType.HEADING:
            line = block.lstrip()
            level = len(line) - len(line.lstrip("#"))
            content = line[level+1:].strip()
            children.append(ParentNode(f"h{level}", text_to_children(content)))

        elif btype == BlockType.CODE:
            lines = block.split("\n")
            code_text = "\n".join(lines[1:-1]) + "\n"
            code_node = LeafNode("code", code_text)
            children.append(ParentNode("pre", [code_node]))

        elif btype == BlockType.QUOTE:
            quote_lines = [line.lstrip("> ").strip() for line in block.splitlines()]
            quote_text = " ".join(quote_lines)
            children.append(ParentNode("blockquote", text_to_children(quote_text)))

        elif btype == BlockType.UNORDERED_LIST:
            items = [
                ParentNode("li", text_to_children(line.lstrip()[2:].strip()))
                for line in block.splitlines()
            ]
            children.append(ParentNode("ul", items))

        elif btype == BlockType.ORDERED_LIST:
            items = []
            for line in block.splitlines():
                content = line.strip().split(". ", 1)[1]
                items.append(ParentNode("li", text_to_children(content)))
            children.append(ParentNode("ol", items))

    return ParentNode("div", children)
