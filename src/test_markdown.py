from markdown_funcs import extract_markdown_images, extract_markdown_links, split_nodes_delimeter

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_markdown_images_with_no_images(self):
    matches = extract_markdown_images(
        "This text contains no images."
    )
    self.assertListEqual([], matches)

def test_extract_markdown_images_with_multiple_images(self):
    matches = extract_markdown_images(
        "Here is an image ![first](https://example.com/first.png) and another ![second](https://example.com/second.png)."
    )
    self.assertListEqual([
        ("first", "https://example.com/first.png"),
        ("second", "https://example.com/second.png")
    ], matches)

def test_extract_markdown_images_with_alternate_syntax(self):
    matches = extract_markdown_images(
        "An alternative image syntax: ![This is an image](https://example.com/image.png)"
    )
    self.assertListEqual([("This is an image", "https://example.com/image.png")], matches)

def test_extract_markdown_images_with_image_title(self):
    matches = extract_markdown_images(
        "A descriptive image ![image title](https://i.imgur.com/zjjcJKZ.png \"Optional title\")"
    )
    self.assertListEqual([("image title", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_markdown_images_with_invalid_urls(self):
    matches = extract_markdown_images(
        "This is a corrupted image ![broken](broken_url)"
    )
    self.assertListEqual([("broken", "broken_url")], matches)

def test_extract_markdown_images_with_linked_image(self):
    matches = extract_markdown_images(
        "[![linked image](https://example.com/image.png)](https://example.com)"
    )
    self.assertListEqual([("linked image", "https://example.com/image.png")], matches)
