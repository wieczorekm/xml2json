from tokens import *

WHITESPACES = (' ', '\t', '\n')


class Lexer:

    def __init__(self, source):
        self.source = source
        self.cursor = 0

    def get_next_token(self):
        try:
            return self.do_get_next_token()
        except IndexError:
            self.throw_unexpected_token_exception()

    def do_get_next_token(self):
        self.shift_cursor_igonoring_whitespaces()
        if self.source[self.cursor] == "<":
            return self.do_get_open_token()
        elif self.source[self.cursor] == "/":
            return self.do_get_close_with_slash_token()
        elif self.source[self.cursor] == ">":
            return self.do_get_close_token()
        elif self.source[self.cursor] == "=":
            return self.do_get_equals_token()
        elif self.source[self.cursor] == '"':
            return self.do_get_quoted_id_token()
        else:
            return self.do_get_id_token()

    def do_get_open_token(self):
        if self.source[self.cursor + 1] == "/":
            self.cursor += 2
            return OpenOfTagWithSlashToken()
        else:
            self.cursor += 1
            return OpenOfTagToken()

    def do_get_close_with_slash_token(self):
        if self.source[self.cursor+1] == ">":
            self.cursor += 2
            return CloseOfTagWithSlashToken()
        else:
            self.throw_unexpected_token_exception()

    def do_get_close_token(self):
        self.cursor += 1
        return CloseOfTagToken()

    def do_get_equals_token(self):
        self.cursor += 1
        return EqualsToken()

    def do_get_id_token(self):
        return IdToken(self.read_id_from_input())

    def do_get_quoted_id_token(self):
        return QuotedIdToken(self.read_quoted_id_from_input())

    def read_id_from_input(self):
        id = ""
        while self.source[self.cursor] not in WHITESPACES and self.source[self.cursor] not in [">", "/", "="]:
            id += self.source[self.cursor]
            self.cursor += 1
        return id

    def read_quoted_id_from_input(self):
        quoted_id = ""
        self.cursor += 1
        while self.source[self.cursor] != '"':
            quoted_id += self.source[self.cursor]
            self.cursor += 1
        self.cursor += 1
        return quoted_id


    def throw_unexpected_token_exception(self):
        raise LexerException("Unexpected end of text near " + str(self.cursor) + " char")

    def shift_cursor_igonoring_whitespaces(self):
        while self.source[self.cursor] in WHITESPACES:
            self.cursor += 1


class LexerException(Exception):
    def __init__(self, message):
        super(LexerException, self).__init__()
        self.message = message


# class EndOfTextException(Exception):
#     def __init__(self):
#         super(EndOfTextException, self).__init__()
