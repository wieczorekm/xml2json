import unittest

from lexer import Lexer, LexerException
from tokens import *


def get_token_from_input(source):
    lexer = Lexer(source)
    token = lexer.get_next_token()
    return token


class LexerTest(unittest.TestCase):

    def test_open_token(self):
        token = get_token_from_input("<")
        self.assertIsInstance(token, OpenOfTagToken)

    def test_open_of_single_tag(self):
        token = get_token_from_input("</")
        self.assertIsInstance(token, OpenOfSingleTagToken)

    def test_close_of_tag(self):
        token = get_token_from_input("/>")
        self.assertIsInstance(token, CloseOfTagToken)

    def test_close_of_single_tag(self):
        token = get_token_from_input(">")
        self.assertIsInstance(token, CloseOfSingleTagToken)


if __name__ == '__main__':
    unittest.main()
