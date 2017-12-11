from src.token import *

WHITESPACES = (' ', '\t', '\n')


class Lexer:

    def __init__(self, source):
        self.source = source
        self.cursor = 0

    def get_next_token(self):
        if self.cursor == len(self.source):
            return EndOfTextToken()
        trimmed = self.trim_whitespaces()
        if self.source[self.cursor:self.cursor+4] == '<!--':
            return self.read_comment()
        elif self.source[self.cursor:self.cursor+2] == '</':
            return self.read_close_tag()
        elif self.source[self.cursor:self.cursor+2] == '<?':
            return self.read_prolog_tag()
        elif self.source[self.cursor] == '<':
            return self.read_open_tag()
        else:
            return self.read_text(trimmed)

    def read_text(self, trimmed):
        # adding trimmed whitespaces to preserve them as text
        value = trimmed
        while self.source[self.cursor] != "<":
            value += self.source[self.cursor]
            self.cursor += 1
        return TextToken(value)

    def read_open_tag(self):
        self.cursor += 1
        return self.get_open_tag()

    def read_prolog_tag(self):
        self.cursor += 2
        return self.get_prolog_tag()

    def read_close_tag(self):
        self.cursor += 2
        return self.get_close_tag()

    def read_comment(self):
        self.cursor += 4
        return CommentToken(self.read_comment_body())

    def read_comment_body(self):
        comment_body = ""
        while self.source[self.cursor:self.cursor + 3] != '-->':
            if self.cursor == len(self.source)-2:
                raise LexerException("Closing comment tag --> expected")
            comment_body += self.source[self.cursor]
            self.cursor += 1
        self.cursor += 3
        return comment_body

    def get_close_tag(self):
        self.trim_whitespaces()
        return CloseTagToken(self.do_get_close_tag())

    def do_get_close_tag(self):
        tag = ""
        while self.source[self.cursor] != ">":
            tag += self.source[self.cursor]
            self.cursor += 1
            if self.source[self.cursor] in WHITESPACES:
                self.trim_whitespaces()
                break
        self.cursor += 1
        return tag

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
                attribute_name = self.parse_attribute_name()
                self.trim_whitespaces()
                attributes[attribute_name] = self.parse_attribute_value()
            self.cursor += 1
        return tag, attributes

    def parse_attribute_value(self):
        if self.source[self.cursor] != "\"":
            raise LexerException("Attribute assignment \" expected")
        self.cursor += 1
        attribute_value = ""
        while self.source[self.cursor] != "\"":
            attribute_value += self.source[self.cursor]
            self.cursor += 1
        return attribute_value

    def parse_attribute_name(self):
        attribute_name = ""
        while self.source[self.cursor] != "=":
            if self.cursor == len(self.source)-1:
                raise LexerException("Attribute assignment = expected")
            attribute_name += self.source[self.cursor]
            self.cursor += 1
            if self.source[self.cursor] in WHITESPACES:
                self.trim_whitespaces()
        self.cursor += 1
        return attribute_name

    def get_prolog_tag(self):
        tag, attributes = self.read_tag_and_attributes(in_prolog=True)
        self.cursor += 2
        return PrologTagToken(tag, attributes)

    def trim_whitespaces(self):
        trimmed = ""
        while self.source[self.cursor] in WHITESPACES:
            trimmed += self.source[self.cursor]
            self.cursor += 1
        return trimmed


class LexerException(Exception):
    def __init__(self, message):
        super(LexerException, self).__init__()
        self.message = message
