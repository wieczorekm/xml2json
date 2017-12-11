from src.token import *


class Lexer:

    def __init__(self, source):
        self.source = source
        self.cursor = 0

    def get_next_token(self):
        if self.source[self.cursor:self.cursor+2] == '</':
            self.cursor += 2
            tag = self.get_tag()
            return CloseTagToken(tag)
        elif self.source[self.cursor] == '<':
            self.cursor += 1
            tag = self.get_tag()
            return OpenTagToken(tag)
        else:
            value = ""
            while self.source[self.cursor] != "<":
                value += self.source[self.cursor]
                self.cursor += 1
            return TextToken(value)

    def get_tag(self):
        tag = ""
        while self.source[self.cursor] != ">":
            tag += self.source[self.cursor]
            self.cursor += 1
        self.cursor += 1
        return tag
