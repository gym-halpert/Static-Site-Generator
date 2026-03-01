import os
import shutil
from textnode import TextType
from textnode import TextNode
from markdown_funcs import *

def main():
#    var = TextNode("This is an anchor", TextType.LINK, "https://www.boot.dev")
#    print(var)
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    source = os.path.join(root, 'static')
    destination = os.path.join(root, 'public')

    public_to_static(source, destination)

    generate_page("content/index.md", "template.html", "public/index.html")

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No header found in markdown file")

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as t:
        template = t.read()
    title = extract_title(markdown)
    node = markdown_to_html_node(markdown)
    html_string = node.to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)
    to_file.close()

def public_to_static(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    copy_recursion(source, destination)

def copy_recursion(source, destination):
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isdir(source_path):
            os.mkdir(destination_path)
            copy_recursion(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)
            print(f'Copied: {source_path} to {destination_path}')

if __name__ == "__main__":
    main()
