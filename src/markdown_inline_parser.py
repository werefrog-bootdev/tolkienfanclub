from textnode import TextNode, TextType
from markdown_inline import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    # Appliquer les séparateurs dans l'ordre : BOLD > ITALIC > CODE
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Puis les images et les liens
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
