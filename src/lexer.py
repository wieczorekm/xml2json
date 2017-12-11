from src.token import *


class Lexer:

    def __init__(self, source):
        self.source = source
        self.cursor = 0

    def get_next_token(self):
        # close tag
        if self.source[self.cursor:self.cursor+2] == '</':
            self.cursor += 2
            tag = self.get_close_tag()
            return CloseTagToken(tag)
        # open tag
        elif self.source[self.cursor] == '<':
            self.cursor += 1
            tag, attributes = self.get_open_tag()
            return OpenTagToken(tag, attributes)
        # text
        else:
            value = ""
            while self.source[self.cursor] != "<":
                value += self.source[self.cursor]
                self.cursor += 1
            return TextToken(value)

    def get_close_tag(self):
        tag = ""
        while self.source[self.cursor] != ">":
            tag += self.source[self.cursor]
            self.cursor += 1
        self.cursor += 1
        return tag

    def get_open_tag(self):
        tag = ""
        attributes = {}
        reading_tag = True
        while self.source[self.cursor] != ">":
            if self.source[self.cursor] == ' ':
                reading_tag = False
                self.cursor += 1
            if reading_tag:
                tag += self.source[self.cursor]
            else:
                attribute_name = ""
                while self.source[self.cursor] != "=":
                    attribute_name += self.source[self.cursor]
                    self.cursor += 1

                # skipping = and opening "
                self.cursor += 1
                self.cursor += 1
                attribute_value = ""
                while self.source[self.cursor] != "\"":
                    attribute_value += self.source[self.cursor]
                    self.cursor += 1

                attributes[attribute_name] = attribute_value
            self.cursor += 1
        self.cursor += 1
        return tag, attributes
