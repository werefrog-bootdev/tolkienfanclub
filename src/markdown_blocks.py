from enum import Enum, auto

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Split a raw Markdown document into block-level elements.

    A block is defined as a section of text separated from others by
    one or more blank lines. This function strips leading/trailing whitespace
    and ignores empty blocks.

    Args:
        markdown (str): The full markdown document as a string.

    Returns:
        list[str]: A list of block strings.
    """
    # Split the markdown into chunks by double newline
    raw_blocks = markdown.split("\n\n")

    # Strip whitespace and filter out empty blocks
    return [block.strip() for block in raw_blocks if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    """
    Determines the type of a markdown block.

    Args:
        block (str): A block of markdown (already stripped of surrounding whitespace).

    Returns:
        BlockType: The type of the block.
    """
    lines = block.split("\n")

    # Code block: starts and ends with ```
    if lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.CODE

    # Heading: 1-6 '#' followed by a space and heading text
    if len(lines) == 1:
        stripped = lines[0].lstrip()
        if stripped.startswith("#") and stripped.count("#") <= 6:
            if stripped[len(stripped.split()[0]):].startswith(" "):
                return BlockType.HEADING

    # Quote block: all lines start with >
    if all(line.lstrip().startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: all lines start with '- '
    if all(line.lstrip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: 1. ..., 2. ..., etc.
    if all(line.lstrip().startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    # Default: paragraph
    return BlockType.PARAGRAPH
