from markdown_funcs import extract_markdown_images, extract_markdown_links, split_nodes_delimeter, split_nodes_link, split_nodes_image

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

def test_split_image(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ],
        new_nodes,
    )

def test_split_image_single(self):
    node = TextNode(
        "![image](https://www.example.COM/IMAGE.PNG)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
        ],
        new_nodes,
    )

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
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
    )

def test_split_links(self):
    node = TextNode(
        "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
            TextNode(" with text that follows", TextType.TEXT),
        ],
        new_nodes,
    )
