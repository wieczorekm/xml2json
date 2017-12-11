from src.lexer import *
import sys

if len(sys.argv) == 2 :
    f = open(sys.argv[1], 'r')
    content = f.read()

    lexer = Lexer(content)
    tokens = lexer.tokenize()

    for token in tokens:
        print(token)
else:
    print("Usage: python main.py <file_to_parse>")