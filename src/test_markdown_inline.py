import unittest
from textnode import TextNode, TextType
from markdown_inline import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


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
            ],
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
            ],
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
            ],
        )

    def test_non_text_type(self):
        node = TextNode("Already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [])


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "An image ![alt](http://img.png) here", TextType.TEXT
        )
        result = split_nodes_image([node])
        self.assertEqual(
            result,
            [
                TextNode("An image ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "http://img.png"),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_multiple_images(self):
        node = TextNode(
            "![a](u1) and ![b](u2)", TextType.TEXT
        )
        result = split_nodes_image([node])
        self.assertEqual(
            result,
            [
                TextNode("a", TextType.IMAGE, "u1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "u2"),
            ],
        )

    def test_image_surrounded_by_text(self):
        node = TextNode(
            "start ![pic](url) end", TextType.TEXT
        )
        result = split_nodes_image([node])
        self.assertEqual(
            result,
            [
                TextNode("start ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "url"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_image_in_non_text_node(self):
        node = TextNode("![a](u)", TextType.BOLD)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode("Visit [here](http://site.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(
            result,
            [
                TextNode("Visit ", TextType.TEXT),
                TextNode("here", TextType.LINK, "http://site.com"),
            ],
        )

    def test_multiple_links(self):
        node = TextNode("Links: [A](u1), [B](u2)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(
            result,
            [
                TextNode("Links: ", TextType.TEXT),
                TextNode("A", TextType.LINK, "u1"),
                TextNode(", ", TextType.TEXT),
                TextNode("B", TextType.LINK, "u2"),
            ],
        )

    def test_link_at_start_and_end(self):
        node = TextNode("[Start](url1) middle [End](url2)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(
            result,
            [
                TextNode("Start", TextType.LINK, "url1"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("End", TextType.LINK, "url2"),
            ],
        )

    def test_link_in_non_text_node(self):
        node = TextNode("[X](y)", TextType.ITALIC)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])


if __name__ == "__main__":
    unittest.main()
