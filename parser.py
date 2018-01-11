from parser_elements import *
from tokens import *


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer

    def get_document_tree(self):
        open_of_tag = self.lexer.get_next_token()
        id_token = self.lexer.get_next_token()
        close_of_tag = self.lexer.get_next_token()
        if isinstance(close_of_tag, CloseOfTagWithSlashToken):
            xml = Xml(id_token.value, None)
        else:  # assuming it is CloseOfTag
            text = self.lexer.get_text_until_open_of_tag()
            open_of_close_tag = self.lexer.get_next_token()
            id_close_tag = self.lexer.get_next_token()
            close_of_close_tag = self.lexer.get_next_token()
            xml = Xml(id_token.value, text)
        return DocumentTree(xml)

    def _raise_unexpected_token_error(self):
        raise ParserException("Unexpected token")


class ParserException(Exception):
    def __init__(self, message):
        super(ParserException, self).__init__()
        self.message = message
