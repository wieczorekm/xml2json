import unittest

from lexer import Lexer, LexerException
from tokens import *


def get_token_from_input(source):
    lexer = Lexer(source)
    token = lexer.get_next_token()
    return token


class LexerTest(unittest.TestCase):

    def test_open_token(self):
        token = get_token_from_input("< ")
        self.assertIsInstance(token, OpenOfTagToken)

    def test_open_of_single_tag(self):
        token = get_token_from_input("</")
        self.assertIsInstance(token, OpenOfSingleTagToken)

    def test_close_of_tag(self):
        token = get_token_from_input("/>")
        self.assertIsInstance(token, CloseOfTagWithSlashToken)

    def test_close_of_single_tag(self):
        token = get_token_from_input(">")
        self.assertIsInstance(token, CloseOfTagToken)

    def test_equals_tag(self):
        token = get_token_from_input("=")
        self.assertIsInstance(token, EqualsToken)

    def test_id_tag(self):
        token = get_token_from_input("xml ")
        self.assertIsInstance(token, IdToken)
        self.assertEqual(token.value, "xml")

    def test_open_tag(self):
        lexer = Lexer("<tag>")
        open_tag = lexer.get_next_token()
        id = lexer.get_next_token()
        close_tag = lexer.get_next_token()
        self.assertIsInstance(open_tag, OpenOfTagToken)
        self.assertIsInstance(id, IdToken)
        self.assertEqual(id.value, "tag")
        self.assertIsInstance(close_tag, CloseOfTagToken)



if __name__ == '__main__':
    unittest.main()
