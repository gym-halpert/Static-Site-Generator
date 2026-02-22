from textnode import TextType
from textnode import TextNode

def main():
    var = TextNode("This is an anchor", TextType.LINK, "https://www.boot.dev")
    print(var)

main()
