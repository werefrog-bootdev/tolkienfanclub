import unittest
from markdown_extract import extract_markdown_images, extract_markdown_links


class TestMarkdownExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "![one](url1) and ![two](url2)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("one", "url1"), ("two", "url2")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a [link](https://example.com) and [another](https://test.com)"
        )
        self.assertListEqual(
            [("link", "https://example.com"), ("another", "https://test.com")],
            matches,
        )

    def test_links_and_images(self):
        text = "![img](imgurl) and [anchor](anchorurl)"
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("img", "imgurl")], img_matches)
        self.assertListEqual([("anchor", "anchorurl")], link_matches)

    def test_no_matches(self):
        self.assertListEqual([], extract_markdown_images("no images here"))
        self.assertListEqual([], extract_markdown_links("no links here"))


if __name__ == "__main__":
    unittest.main()
