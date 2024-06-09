import unittest
from block_markdown import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_normal_markdown(self):
        markdown = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is a list item\n* This is another list item"
        blocks = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is a list item\n* This is another list item'
        ]
        self.assertEqual(markdown_to_blocks(markdown), blocks)

    def test_leading_whitespace(self):
        markdown = "     # This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n     * This is a list item\n* This is another list item"
        blocks = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is a list item\n* This is another list item'
        ]
        self.assertEqual(markdown_to_blocks(markdown), blocks)

    def test_trailing_whitespace(self):
        markdown = "# This is a heading   \n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.          \n\n* This is a list item\n* This is another list item"
        blocks = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is a list item\n* This is another list item'
        ]
        self.assertEqual(markdown_to_blocks(markdown), blocks)

    def test_hectic_whitespace(self):
        markdown = "# This is a heading   \n   \nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.   \n \n    * This is a list item  \n * This is another list item"
        blocks = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is a list item\n* This is another list item'
        ]
        self.assertEqual(markdown_to_blocks(markdown), blocks)

    def test_block_to_block(self):
        blocks = [
            'This is a paragraph',
            '# This is a heading',
            '```This is a code block```',
            '>This is a quote\n>something inspirational',
            '* This is an unordered list\n* it has more than one line',
            '1. This is an ordered list\n2. it has more than one line'
        ]
        expected_types = [
            block_type_paragraph,
            block_type_heading,
            block_type_code,
            block_type_quote,
            block_type_unordered_list,
            block_type_ordered_list
        ]
        for block, expected_type in zip(blocks, expected_types):
            self.assertEqual(block_to_block_type(block), expected_type)

    def test_block_to_html(self):
        blocks = [
            'This is a paragraph',
            '# This is a heading',
            '## This is another heading',
            '### This is again another heading',
            '```This is a code block```',
            '>This is a quote\n>something inspirational',
            '* This is an unordered list\n* it has more than one line',
            '1. This is an ordered list\n2. it has more than one line'
        ]
        expected_outputs = [
            '<div><p>This is a paragraph</p></div>',
            '<div><h1>This is a heading</h1></div>',
            '<div><h2>This is another heading</h2></div>',
            '<div><h3>This is again another heading</h3></div>',
            '<div><pre><code>This is a code block</code></pre></div>',
            '<div><blockquote>This is a quote something inspirational</blockquote></div>',
            '<div><ul><li>This is an unordered list</li><li>it has more than one line</li></ul></div>',
            '<div><ol><li>This is an ordered list</li><li>it has more than one line</li></ol></div>'
        ]

        for block, expected_output in zip(blocks, expected_outputs):
            node = markdown_to_html_node(block)
            self.assertEqual(node.to_html(), expected_output)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
