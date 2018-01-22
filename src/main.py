from src.lexer import Lexer
from src.parser import Parser
import sys
import json

from src.translator import Translator

if len(sys.argv) == 3:
    f = open(sys.argv[1], 'r')
    content = f.read()

    f = open(sys.argv[2], 'r')

    config = json.loads(f.read())

    lexer = Lexer(content)
    parser = Parser(lexer)
    document_tree = parser.get_document_tree()

    translator = Translator(document_tree, config)
    json = translator.get_json()

    output_file = open("output.json", "w")
    output_file.write(json)
    output_file.close()


else:
    print("Usage: python main.py <file_to_translate> <config_file>")
