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
