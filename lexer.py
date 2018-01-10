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
        if self.source[self.cursor] == "<":
            if self.source[self.cursor+1] == "/":
                self.cursor += 2
                return OpenOfSingleTagToken()
            else:
                self.cursor += 1
                return OpenOfTagToken()
        elif self.source[self.cursor] == "/":
            if self.source[self.cursor+1] == ">":
                self.cursor += 2
                return CloseOfTagWithSlashToken()

            else:
                self.throw_unexpected_token_exception()
        elif self.source[self.cursor] == ">":
            self.cursor += 1
            return CloseOfTagToken()
        elif self.source[self.cursor] == "=":
            self.cursor += 1
            return EqualsToken()
        else:
            id = self.get_id_from_input()
            return IdToken(id)

    def get_id_from_input(self):
        id = ""
        while self.source[self.cursor] not in WHITESPACES and self.source[self.cursor] != ">":
            id += self.source[self.cursor]
            self.cursor += 1
        return id

    def throw_unexpected_token_exception(self):
        raise LexerException("Unexpected end of text near " + str(self.cursor) + " char")


class LexerException(Exception):
    def __init__(self, message):
        super(LexerException, self).__init__()
        self.message = message


# class EndOfTextException(Exception):
#     def __init__(self):
#         super(EndOfTextException, self).__init__()
