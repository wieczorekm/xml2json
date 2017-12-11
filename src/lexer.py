from src.token import *


class Lexer:

    def __init__(self, source):
        self.source = source

    def get_next_token(self):
        if self.source[0:2] == '</':
            return CloseTagToken()
        elif self.source[0] == '<':
            return OpenTagToken()
        else:
            return TextToken()
