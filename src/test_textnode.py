import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_default_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)
    
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_different_text(self):
        node1 = TextNode("Text one", TextType.BOLD)
        node2 = TextNode("Text two", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_text_type(self):
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_equal_different_url(self):
        node1 = TextNode("Same text", TextType.BOLD, url=None)
        node2 = TextNode("Same text", TextType.BOLD, url="http://example.com")
        self.assertNotEqual(node1, node2)

    def test_equal_with_url(self):
        node1 = TextNode("Text", TextType.LINK, url="http://example.com")
        node2 = TextNode("Text", TextType.LINK, url="http://example.com")
        self.assertEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
