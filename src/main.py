import os
import shutil
from textnode import TextType
from textnode import TextNode

def main():
#    var = TextNode("This is an anchor", TextType.LINK, "https://www.boot.dev")
#    print(var)
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    source = os.path.join(root, 'static')
    destination = os.path.join(root, 'public')

    public_to_static(source, destination)

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
