import re
from textnode import TextNode, TextType


RE_IMAGE = re.compile(r"!\[(?P<alt>[^\]]+)\]\((?P<url>[^)]+)\)")
RE_LINK = re.compile(r"(?<!\!)\[(?P<text>[^\]]+)\]\((?P<url>[^)]+)\)")



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) == 1:
            if node.text != "":
                new_nodes.append(node)
            continue

        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                if part != "":
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                if part != "":
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        for match in RE_IMAGE.finditer(text):
            start, end = match.span()
            # Ajoute le texte avant l'image
            if start > last_index:
                before = text[last_index:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
            # Ajoute l'image avec les groupes nommés
            alt = match.group("alt")
            url = match.group("url")
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            last_index = end
        # Ajoute le texte après la dernière image
        if last_index < len(text):
            after = text[last_index:]
            if after:
                new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0
        for match in RE_LINK.finditer(text):
            start, end = match.span()
            # Ajoute le texte avant le lien
            if start > last_index:
                before = text[last_index:start]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
            # Ajoute le lien avec les groupes nommés
            link_text = match.group("text")
            url = match.group("url")
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_index = end
        # Ajoute le texte après le dernier lien
        if last_index < len(text):
            after = text[last_index:]
            if after:
                new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes
