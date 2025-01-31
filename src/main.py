from textnode import TextNode, TextType

def main():
    test = TextNode("Test Text", TextType.BOLD, url='test.example.url')
    print(test)

main()

