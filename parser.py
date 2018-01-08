from parser_elements import *
from tokens import *


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer

    def get_document_tree(self):
        first_tag = self.lexer.get_next_token()

        if isinstance(first_tag, OpenTagToken):
            text = self.lexer.get_next_token()
            closetag = self.lexer.get_next_token()
            if first_tag.tag != closetag.tag:
                raise ParserException("Opentag tag: " + first_tag.tag + " doesn't match closetag tag: " + closetag.tag)
            xml = Xml(first_tag.tag, text.value, first_tag.attributes)
        else:  # for now it is SingleTag
            xml = Xml(first_tag.tag, None, first_tag.attributes)
        return DocumentTree(xml)


class ParserException(Exception):
    def __init__(self, message):
        super(ParserException, self).__init__()
        self.message = message
