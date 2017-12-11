from src.token import *

WHITESPACES = (' ', '\t', '\n')


class Lexer:

    def __init__(self, source):
        self.source = source
        self.cursor = 0

    def get_next_token(self):
        if self.cursor == len(self.source):
            return EndOfTextToken()
        self.trim_whitespaces()
        # close tag
        if self.source[self.cursor:self.cursor+2] == '</':
            self.cursor += 2
            return self.get_close_tag()

        #prolog tag
        elif self.source[self.cursor:self.cursor+2] == '<?':
            self.cursor += 2
            return self.get_prolog_tag()

        # open tag
        elif self.source[self.cursor] == '<':
            self.cursor += 1
            return self.get_open_tag()
        # text
        else:
            value = ""
            while self.source[self.cursor] != "<":
                value += self.source[self.cursor]
                self.cursor += 1
            return TextToken(value)

    def get_close_tag(self):
        self.trim_whitespaces()
        tag = ""
        while self.source[self.cursor] != ">":
            tag += self.source[self.cursor]
            self.cursor += 1
            if self.source[self.cursor] in WHITESPACES:
                self.trim_whitespaces()
                break
        #todo check if this is >
        self.cursor += 1
        return CloseTagToken(tag)

    def get_open_tag(self):
        tag, attributes = self.read_tag_and_attributes(in_prolog=False)
        if self.source[self.cursor] == "/":
            self.cursor += 2
            return SingleTagToken(tag, attributes)
        else:
            self.cursor += 1
            return OpenTagToken(tag, attributes)

    def read_tag_and_attributes(self, in_prolog):
        self.trim_whitespaces()
        tag = ""
        attributes = {}
        reading_tag = True

        before_last_char = "?" if in_prolog else "/"
        while self.source[self.cursor] != ">" and self.source[self.cursor] != before_last_char:
            if self.source[self.cursor] in WHITESPACES:
                reading_tag = False
                self.trim_whitespaces()
                continue
            if reading_tag:
                tag += self.source[self.cursor]
            else:
                attribute_name = ""
                while self.source[self.cursor] != "=":
                    attribute_name += self.source[self.cursor]
                    self.cursor += 1
                    if self.source[self.cursor] in WHITESPACES:
                        self.trim_whitespaces()

                # todo check if this is =
                self.cursor += 1

                self.trim_whitespaces()

                # todo check if this is "
                self.cursor += 1
                attribute_value = ""
                while self.source[self.cursor] != "\"":
                    attribute_value += self.source[self.cursor]
                    self.cursor += 1

                attributes[attribute_name] = attribute_value
            self.cursor += 1
        return tag, attributes

    def get_prolog_tag(self):
        tag, attributes = self.read_tag_and_attributes(in_prolog=True)
        self.cursor += 2
        return PrologTagToken(tag, attributes)


    def trim_whitespaces(self):
        while self.source[self.cursor] in WHITESPACES:
            self.cursor += 1
