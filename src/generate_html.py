import os

from block_markdown import markdown_to_html_node


def generate_page(from_markdown, to_html, with_template):
    print(f"Generating page from {from_markdown} to {to_html} using {with_template} as template")
    title = extract_title(from_markdown)
    get_title = ""
    with open(with_template, "r") as template_file:
        template = template_file.read()
        get_title = template
    replace_title = get_title.replace(' {{ Title }} ', title)
    content = ""
    with open(from_markdown, "r") as markdown_file:
        markdown = markdown_file.read()
        content =  markdown
    new_content = markdown_to_html_node(content).to_html()
    replace_content = replace_title.replace('{{ Content }}', new_content)
    with open(to_html, "w") as html_file:
        html_file.write(replace_content)


def generate_pages_recursive(from_content_dir, to_html_dir, with_template):
    if os.path.exists(from_content_dir):
        if not os.path.exists(to_html_dir):
            os.mkdir(to_html_dir)
        for item in os.listdir(from_content_dir):
            from_item_path = os.path.join(from_content_dir, item)
            to_item_path = os.path.join(to_html_dir, item)
            if os.path.isdir(from_item_path):
                if not os.path.exists(to_item_path):
                    os.mkdir(to_item_path)
                generate_pages_recursive(from_item_path, to_item_path, with_template)
            elif from_item_path.endswith('.md'):
                html_path = to_item_path.replace('.md', '.html')
                generate_page(from_item_path, html_path, with_template)
    else:
        raise Exception("Error: content directory does not exist")
        

def extract_title(file_path):
    with open(file_path, "r") as file:
        title = file.readline()
        if title.startswith("# "):
            return title.lstrip("# ").strip()
        else:
            raise Exception("Failed to read title")
