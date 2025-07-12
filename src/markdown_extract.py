import re


def extract_markdown_images(text):
    # Matches ![alt](url)
    return re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", text)


def extract_markdown_links(text):
    # Matches [text](url) but not images
    return re.findall(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)", text)
