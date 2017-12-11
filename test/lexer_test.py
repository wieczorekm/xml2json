import unittest

from src.lexer import Lexer
from src.token import *


def get_token_from_input(source):
    lexer = Lexer(source)
    token = lexer.get_next_token()
    return token


class LexerTest(unittest.TestCase):

    def test_type_xml_open_tag(self):
        token = get_token_from_input("<sample>")
        self.assertIsInstance(token, OpenTagToken)

    def test_type_xml_close_tag(self):
        token = get_token_from_input("</sample>")
        self.assertIsInstance(token, CloseTagToken)

    def test_type_text(self):
        token = get_token_from_input("text")
        self.assertIsInstance(token, TextToken)


if __name__ == '__main__':
    unittest.main()