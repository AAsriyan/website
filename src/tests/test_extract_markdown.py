import unittest
from markdown_utils import extract_markdown_images, extract_markdown_links	

class TestExtractMarkdown(unittest.TestCase):
	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
				"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_images_multiple(self):
		matches = extract_markdown_images(
			"Text ![img1](url1) and ![img2](url2)"
		)
		self.assertListEqual([
			("img1", "url1"),
			("img2", "url2")
		], matches)

	def test_extract_markdown_images_empty(self):
		matches = extract_markdown_images("No images here!")
		self.assertListEqual([], matches)

	def test_extract_markdown_images_edge_cases(self):
		matches = extract_markdown_images("![alt]() and ![](url)")
		self.assertListEqual([
			("alt", ""),
			("", "url")
		], matches)

	def test_extract_markdown_links_single(self):
		matches = extract_markdown_links(
			"This is a [link](https://example.com)"
		)
		self.assertListEqual([
			("link", "https://example.com")
		], matches)

	def test_extract_markdown_links_multiple(self):
		matches = extract_markdown_links(
			"[one](url1) and [two](url2)"
		)
		self.assertListEqual([
			("one", "url1"),
			("two", "url2")
		], matches)

	def test_extract_markdown_links_ignores_images(self):
		matches = extract_markdown_links(
			"![img](imgurl) and [link](url)"
		)
		self.assertListEqual([
			("link", "url")
		], matches)

	def test_extract_markdown_links_edge_cases(self):
		matches = extract_markdown_links("[](url) and [alt]()")
		self.assertListEqual([
			("", "url"),
			("alt", "")
		], matches)

if __name__ == "__main__":
    unittest.main()