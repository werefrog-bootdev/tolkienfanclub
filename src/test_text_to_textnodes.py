import unittest
from textnode import TextNode, TextType
from text_to_nodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_full_conversion(self):
        """Test a full markdown conversion with various text types."""
        markdown = (
            "This is **Elvish** with an _ancient_ word and a `magic spell` and an "
            "![Andúril](https://i.imgur.com/anduril.png) and a "
            "[map](https://lotr.fandom.com/wiki/Middle-earth)"
        )


        result = text_to_textnodes(markdown)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("Elvish", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("ancient", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("magic spell", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("Andúril", TextType.IMAGE, "https://i.imgur.com/anduril.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("map", TextType.LINK, "https://lotr.fandom.com/wiki/Middle-earth"),
        ]


        self.assertEqual(result, expected)
