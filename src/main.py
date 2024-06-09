from copy_contents import copy_contents
from generate_html import generate_pages_recursive


static_dir_path = "./static"
public_dir_path = "./public"
content_dir_path = "./content"
template_path = "./template.html"


def main():
    copy_contents(static_dir_path, public_dir_path)
    generate_pages_recursive(content_dir_path, public_dir_path, template_path)


main()
