import unittest

from markdown_blocks import (
    BlockType, markdown_to_blocks, block_to_block_type
)




MD = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

MD_SPACES = """

   This is a paragraph with leading spaces    




  - List item one    
  - List item two  

"""


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = MD

        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]

        self.assertEqual(markdown_to_blocks(md), expected)

    def test_blocks_are_stripped(self):
        md = MD_SPACES

        expected = [
            "This is a paragraph with leading spaces",
            "- List item one    \n  - List item two",
        ]

        self.assertEqual(markdown_to_blocks(md), expected)


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_blocks(self):
        self.assertEqual(block_to_block_type("# Title"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Subtitle"), BlockType.HEADING)

    def test_code_block(self):
        code = "```\ndef hello():\n    return 'world'\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote_block(self):
        block = "> line one\n> line two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is a normal paragraph.\nIt spans multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_ordered_list(self):
        block = "1. first\n3. wrong"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

 
if __name__ == "__main__":
    unittest.main()
