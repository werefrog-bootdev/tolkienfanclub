import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("Just text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_single_delimiter(self):
        node = TextNode("Hello **world**!", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ]
        )

    def test_multiple_delimiters(self):
        node = TextNode("A _quick_ brown _fox_", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            result,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("quick", TextType.ITALIC),
                TextNode(" brown ", TextType.TEXT),
                TextNode("fox", TextType.ITALIC),
            ]
        )

    def test_code_delimiter(self):
        node = TextNode("Run `ls -la` in terminal", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("ls -la", TextType.CODE),
                TextNode(" in terminal", TextType.TEXT),
            ]
        )

    def test_non_text_type(self):
        node = TextNode("Already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
