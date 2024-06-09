import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Example where props have multiple attributes
        node = HTMLNode(tag="a", value=None, children=None, props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        
        # Example where props are empty
        node = HTMLNode(tag="p", value=None, children=None, props={})
        self.assertEqual(node.props_to_html(), '')
        
        # Example where props is None
        node = HTMLNode(tag="p", value=None, children=None, props=None)
        # Check if the method handles None gracefully, assuming you need to handle it in your method
        self.assertEqual(node.props_to_html(), '')

    def test_leafnode(self):
        node = LeafNode(tag="a", value="Click the link!", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Click the link!</a>')

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
