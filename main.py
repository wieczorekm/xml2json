from lexer import Lexer
from parser import Parser
import sys


if len(sys.argv) == 2:
    f = open(sys.argv[1], 'r')
    content = f.read()

    lexer = Lexer(content)
    parser = Parser(lexer)

    document_tree = parser.get_document_tree()
    pass


else:
    print("Usage: python main.py <file_to_parse>")
