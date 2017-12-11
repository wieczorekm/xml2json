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
        token = get_token_from_input("text<")
        self.assertIsInstance(token, TextToken)

    def test_value_xml_open_tag(self):
        token = get_token_from_input("<sample>")
        self.assertEqual(token.tag, "sample")

    def test_value_xml_close_tag(self):
        token = get_token_from_input("</sample>")
        self.assertEqual(token.tag, "sample")

    def test_value_text_tag(self):
        token = get_token_from_input("text<") # < is as begin of new xml closing tag
        self.assertEqual(token.value, "text")

    def test_two_open_tags(self):
        source = "<first><second>"
        lexer = Lexer(source)
        self._assertOpenTagToken(lexer.get_next_token(), "first")
        self._assertOpenTagToken(lexer.get_next_token(), "second")

    def test_two_close_tags(self):
        source = "</first></second>"
        lexer = Lexer(source)
        self._assertCloseTagToken(lexer.get_next_token(), "first")
        self._assertCloseTagToken(lexer.get_next_token(), "second")

    def test_simple_xml(self):
        source = "<sample>text</sample>"
        lexer = Lexer(source)
        self._assertOpenTagToken(lexer.get_next_token(), "sample")
        self._assertTextToken(lexer.get_next_token(), "text")
        self._assertCloseTagToken(lexer.get_next_token(), "sample")

    def test_tag_for_open_tag_with_attribute(self):
        token = get_token_from_input('<sample attr="value">')
        self._assertOpenTagToken(token, "sample")

    def test_attribute_for_open_tag_with_attribute(self):
        token = get_token_from_input('<sample attr="value">')
        self.assertEqual(len(token.attributes), 1)
        self.assertEqual(token.attributes['attr'], 'value')

    def _assertOpenTagToken(self, token, token_tag):
        self.assertIsInstance(token, OpenTagToken)
        self.assertEqual(token.tag, token_tag)

    def _assertCloseTagToken(self, token, token_tag):
        self.assertIsInstance(token, CloseTagToken)
        self.assertEqual(token.tag, token_tag)

    def _assertTextToken(self, token, token_value):
        self.assertIsInstance(token, TextToken)
        self.assertEqual(token.value, token_value)


if __name__ == '__main__':
    unittest.main()