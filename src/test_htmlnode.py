import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
