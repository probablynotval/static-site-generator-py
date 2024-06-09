import re

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "ulist"
block_type_ordered_list = "olist"


def markdown_to_blocks(markdown):
    fix_markdown = "\n".join(bad_block.strip() for bad_block in markdown.splitlines()) # this fixes cases of hectic whitespace, such as whitespace between newlines, e.g. '\n   \n'
    split_markdown = fix_markdown.split("\n\n")
    new_blocks = []
    for old_block in split_markdown:
        if not old_block:
            continue
        new_blocks.append(old_block.strip())
    return new_blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == "paragraph":
        return markdown_paragraph_to_html(block)
    if block_type == "heading":
        return markdown_heading_to_html(block)
    if block_type == "code":
        return markdown_code_to_html(block)
    if block_type == "quote":
        return markdown_quote_to_html(block)
    if block_type == "ulist":
        return markdown_ulist_to_html(block)
    if block_type == "olist":
        return markdown_olist_to_html(block)
    raise ValueError(f"Unknown block type: {block_type}")


def block_to_block_type(block):
    if block.startswith("#"):
        parts = block.split(" ", 1)
        if not (len(parts) > 1 and parts[0].count("#") == len(parts[0])):
            return
        if 1 <= len(parts[0]) <= 6:
            return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    if all(line.startswith(">") for line in block.splitlines()):
        return block_type_quote
    if block.startswith("* "):
        for line in block.splitlines():
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_unordered_list
    if block.startswith("- "):
        for line in block.splitlines():
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_unordered_list
    if all(re.match(r"^(\d+)\. ", line) for line in block.splitlines()):
        expected_number = 1
        for line in block.splitlines():
            number = re.match(r"^(\d+)\. ", line)
            if number is None or int(number.group(1)) != expected_number:
                break
            expected_number += 1
        else:
            return block_type_ordered_list
    return block_type_paragraph


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_paragraph_to_html(block):
    paragraph = " ".join(block.splitlines())
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def markdown_heading_to_html(block):
    split_heading = block.split(" ", 1)
    heading_num = split_heading[0].count("#")
    heading_name = split_heading[1]
    children = text_to_children(heading_name)
    if heading_num >= 1 and heading_num <= 6:
        return ParentNode(f"h{heading_num}", children)
    else:
        raise ValueError(f"Heading {heading_num} is not a valid heading")


def markdown_code_to_html(block):
    code = block.strip('`')
    children = text_to_children(code)
    code_node = ParentNode("code", children)
    return ParentNode("pre", [code_node])


def markdown_quote_to_html(block):
    lines = block.splitlines()
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    quote = " ".join(new_lines)
    children = text_to_children(quote)
    return ParentNode("blockquote", children)


def markdown_ulist_to_html(block):
    split_ulist = block.splitlines()
    ulist_item_list = []
    for item in split_ulist:
        ulist_item_text = item.lstrip("* ")
        children = text_to_children(ulist_item_text)
        ulist_item_list.append(ParentNode("li", children))
    # ulist_items = "\n".join(ulist_item_list).replace('\n', '')
    return ParentNode("ul", ulist_item_list)


def markdown_olist_to_html(block):
    split_olist = block.splitlines()
    olist_item_list = []
    for item in split_olist:
        olist_item_text = re.sub(r"^(\d+)\. ", '', item)
        children = text_to_children(olist_item_text)
        olist_item_list.append(ParentNode("li", children))
    # olist_items = "\n".join(olist_item_list).replace('\n', '')
    return ParentNode("ol", olist_item_list)
