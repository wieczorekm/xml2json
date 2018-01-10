from tokens import *

WHITESPACES = (' ', '\t', '\n')


class Lexer:

    def __init__(self, source):
        self.source = source
        self.cursor = 0

    def get_next_token(self):
        if self.source[0:2] == "</":
            return OpenOfSingleTagToken()
        elif self.source[0:2] == "/>":
            return CloseOfTagToken()
        elif self.source[0:1] == ">":
            return CloseOfSingleTagToken()
        return OpenOfTagToken()



class LexerException(Exception):
    def __init__(self, message):
        super(LexerException, self).__init__()
        self.message = message


# class EndOfTextException(Exception):
#     def __init__(self):
#         super(EndOfTextException, self).__init__()
