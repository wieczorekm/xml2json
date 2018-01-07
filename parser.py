from parser_elements import *


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer

    def get_document_tree(self):
        opentag = self.lexer.get_next_token()
        text = self.lexer.get_next_token()
        closetag = self.lexer.get_next_token()
        if opentag.tag != closetag.tag:
            raise ParserException("Opentag tag: " + opentag.tag + " doesn't match closetag tag: " + closetag.tag)
        xml = Xml(opentag.tag, text.value)

        return DocumentTree(xml)


class ParserException(Exception):
    def __init__(self, message):
        super(ParserException, self).__init__()
        self.message = message
