import unittest
from markdown_extract import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_html_node
)



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


class TestMarkdownToHtmlNode(unittest.TestCase):
    PARAGRAPH_MD = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""

    CODEBLOCK_MD = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""

    HEADING_MD = "# Welcome to Middle-earth"

    UNORDERED_LIST_MD = "- The Shire\n- Rivendell\n- Mordor"

    ORDERED_LIST_MD = "1. Frodo\n2. Sam\n3. Gollum"

    QUOTE_MD = "> Even the smallest person can change the course of the future."

    def test_paragraphs(self):
        html = markdown_to_html_node(self.PARAGRAPH_MD).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        html = markdown_to_html_node(self.CODEBLOCK_MD).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        html = markdown_to_html_node(self.HEADING_MD).to_html()
        self.assertEqual(
            html,
            "<div><h1>Welcome to Middle-earth</h1></div>"
        )

    def test_unordered_list(self):
        html = markdown_to_html_node(self.UNORDERED_LIST_MD).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>The Shire</li><li>Rivendell</li><li>Mordor</li></ul></div>"
        )

    def test_ordered_list(self):
        html = markdown_to_html_node(self.ORDERED_LIST_MD).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Frodo</li><li>Sam</li><li>Gollum</li></ol></div>"
        )

    def test_quote(self):
        html = markdown_to_html_node(self.QUOTE_MD).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Even the smallest person can change the course of the future.</blockquote></div>"
        )


if __name__ == "__main__":
    unittest.main()
