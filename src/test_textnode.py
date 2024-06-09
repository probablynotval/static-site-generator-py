import unittest


from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq_text(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_not_eq_text(self):
        node1 = TextNode("This text node is not the...", "bold")
        node2 = TextNode("...same as the other text node", "italic")
        self.assertNotEqual(node1, node2)

    def test_eq_url(self):
        node1 = TextNode("This is another text node", "italic", "https://www.boot.dev/")
        node2 = TextNode("This is another text node", "italic", "https://www.boot.dev/")
        self.assertEqual(node1, node2)
    
    def test_eq_url_none(self):
        node1 = TextNode("This is yet another text node", "bold", None)
        node2 = TextNode("This is yet another text node", "bold", None)
        self.assertEqual(node1, node2)

    def test_not_eq_url(self):
        node1 = TextNode("The text here is the same but url not", "bold", None)
        node2 = TextNode("The text here is the same but url not", "bold", "https://www.boot.dev/")
        self.assertNotEqual(node1, node2)

    def test_not_eq_type(self):
        node1 = TextNode("The text here is the same but the type is not", "italic")
        node2 = TextNode("The text here is the same but the type is not", "bold")
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
