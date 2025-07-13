import unittest

from markdown_parser import markdown_to_blocks



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


if __name__ == "__main__":
    unittest.main()
