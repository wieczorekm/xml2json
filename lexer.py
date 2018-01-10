from tokens import *

WHITESPACES = (' ', '\t', '\n')


class Lexer:
    def __init__(self, source):
        self.source = source
        self.cursor = 0

    def get_next_token(self):
        if self.cursor == len(self.source):
            return EndOfTextToken()
        try:
            return self._do_get_next_token()
        except IndexError:
            self._throw_unexpected_token_exception()

    def get_text_until_open_of_tag(self):
        text = ""
        while self.source[self.cursor] != '<':
            text += self.source[self.cursor]
            self.cursor += 1
        return text

    # also returns read whitespaces as they may be necessary for parser
    def is_next_nonempty_char_an_open_of_tag(self):
        buffer = ""
        while self.source[self.cursor] in WHITESPACES:
            buffer += self.source[self.cursor]
            self.cursor += 1
        return self.source[self.cursor] == "<", buffer

    def _do_get_next_token(self):
        self._shift_cursor_igonoring_whitespaces()
        if self.source[self.cursor] == "<":
            return self._do_get_open_token()
        elif self.source[self.cursor] == "/":
            return self._do_get_close_with_slash_token()
        elif self.source[self.cursor] == "?":
            return self._do_get_close_prolog_token()
        elif self.source[self.cursor] == ">":
            return self._do_get_close_token()
        elif self.source[self.cursor] == "=":
            return self._do_get_equals_token()
        elif self.source[self.cursor] == '"':
            return self._do_get_quoted_id_token()
        elif self.source[self.cursor] == "-":
            return self._do_get_close_of_comment_tag()
        else:
            return self._do_get_id_token()

    def _do_get_open_token(self):
        if self.cursor == len(self.source) - 1 or self.source[self.cursor + 1] not in ["/", "?", "!"]:
            self.cursor += 1
            return OpenOfTagToken()
        elif self.source[self.cursor + 1] == "?":
            self.cursor += 2
            return OpenOfPrologTagToken()
        elif self.source[self.cursor + 1 : self.cursor+4] == "!--":
            self.cursor += 4
            return OpenOfCommentTagToken()
        else:
            self.cursor += 2
            return OpenOfTagWithSlashToken()

    def _do_get_close_with_slash_token(self):
        if self.source[self.cursor + 1] == ">":
            self.cursor += 2
            return CloseOfTagWithSlashToken()
        else:
            self._throw_unexpected_token_exception()

    def _do_get_close_prolog_token(self):
        if self.source[self.cursor + 1] == ">":
            self.cursor += 2
            return CloseOfPrologTagToken()
        else:
            self._throw_unexpected_token_exception()

    def _do_get_close_token(self):
        self.cursor += 1
        return CloseOfTagToken()

    def _do_get_equals_token(self):
        self.cursor += 1
        return EqualsToken()

    def _do_get_id_token(self):
        return IdToken(self._read_id_from_input())

    def _do_get_quoted_id_token(self):
        return QuotedIdToken(self._read_quoted_id_from_input())

    def _do_get_close_of_comment_tag(self):
        if self.source[self.cursor + 1:self.cursor + 3] == "->":
            return CloseOfCommentTagToken()
        else:
            self._throw_unexpected_token_exception()

    def _read_id_from_input(self):
        id = ""
        while self.source[self.cursor] not in WHITESPACES and self.source[self.cursor] not in [">", "/", "="]:
            id += self.source[self.cursor]
            self.cursor += 1
        return id

    def _read_quoted_id_from_input(self):
        quoted_id = ""
        self.cursor += 1
        while self.source[self.cursor] != '"':
            quoted_id += self.source[self.cursor]
            self.cursor += 1
        self.cursor += 1
        return quoted_id

    def _throw_unexpected_token_exception(self):
        raise LexerException("Unexpected end of text near " + str(self.cursor) + " char")

    def _shift_cursor_igonoring_whitespaces(self):
        while self.source[self.cursor] in WHITESPACES:
            self.cursor += 1


class LexerException(Exception):
    def __init__(self, message):
        super(LexerException, self).__init__()
        self.message = message
