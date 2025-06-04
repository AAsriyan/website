import unittest

from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        nodes = [TextNode("Hello world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [TextNode("Hello world", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_single_delimiter_pair(self):
        nodes = [TextNode("Hello *world*!!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("!!", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiter_pairs(self):
        nodes = [TextNode("A *B* C *D* E", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("B", TextType.BOLD),
            TextNode(" C ", TextType.TEXT),
            TextNode("D", TextType.BOLD),
            TextNode(" E", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises(self):
        nodes = [TextNode("Hello *world!!", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "*", TextType.BOLD)

    def test_non_texttype_nodes_unchanged(self):
        nodes = [TextNode("Hello", TextType.BOLD), TextNode("World", TextType.ITALIC)]
        result = split_nodes_delimiter(nodes, "*", TextType.CODE)
        self.assertEqual(result, nodes)

    def test_empty_list(self):
        result = split_nodes_delimiter([], "*", TextType.CODE)
        self.assertEqual(result, [])

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("No images here!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_non_texttype_nodes_unchanged(self):
        node = TextNode("img", TextType.IMAGE, "url")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode("No links here!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_non_texttype_nodes_unchanged(self):
        node = TextNode("link", TextType.LINK, "url")
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        from main import text_to_textnodes
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
