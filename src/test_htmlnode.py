import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), 'href="https://example.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(props={"class": "bold", "id": "main"})
        result = node.props_to_html()
        # Order is not guaranteed, so check both possibilities
        self.assertTrue(
            result == 'class="bold" id="main"' or result == 'id="main" class="bold"'
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_none_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_raises_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode("span", None)

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode("span", "Styled text", {"class": "highlight", "id": "main"})
        result = node.to_html()
        # Order of props is not guaranteed
        self.assertTrue(
            result == '<span class="highlight" id="main">Styled text</span>' or
            result == '<span id="main" class="highlight">Styled text</span>'
        )

if __name__ == "__main__":
    unittest.main()
        