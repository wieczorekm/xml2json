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

    def test_xml_1(self):
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

    def test_tag_for_open_tag_with_two_attributes(self):
        token = get_token_from_input('<sample attr="value" second-attr="another">')
        self._assertOpenTagToken(token, "sample")

    def test_attributes_for_open_tag_with_two_attributes(self):
        token = get_token_from_input('<sample attr="value" second-attr="another">')
        self.assertEqual(len(token.attributes), 2)
        self.assertEqual(token.attributes['attr'], 'value')
        self.assertEqual(token.attributes['second-attr'], 'another')

    def test_type_single_tag(self):
        token = get_token_from_input('<sample/>')
        self._assertSingleTagToken(token, "sample")

    def test_attributes_for_single_tag(self):
        token = get_token_from_input('<sample one="1" two="2"/>')
        self.assertEqual(len(token.attributes), 2)
        self.assertEqual(token.attributes['one'], '1')
        self.assertEqual(token.attributes['two'], '2')

    def test_trims_whitespaces_in_opening_tag_at_end(self):
        tokens = [get_token_from_input('<sample >'),
                  get_token_from_input('<sample  >'),
                  get_token_from_input('<sample\t>'),
                  get_token_from_input('<sample\n>'),
                  get_token_from_input('<sample  \n \t  \t>')]
        for token in tokens:
            self.assertEqual(token.tag, "sample")

    def test_trims_whitespaces_in_opening_tag_at_begin(self):
        tokens = [get_token_from_input('< sample>'),
                  get_token_from_input('<  sample>'),
                  get_token_from_input('<\tsample>'),
                  get_token_from_input('<\t\n\nsample>')]
        for token in tokens:
            self.assertEqual(token.tag, "sample")

    def test_trims_whitespaces_between_attributes(self):
        tokens = [get_token_from_input('<sample  one="1" two="2"/>'),
                  get_token_from_input('<sample  one ="1" two="2"/>'),
                  get_token_from_input('<sample  one = "1" two="2"/>'),
                  get_token_from_input('<sample  one = "1"   two="2"/>'),
                  get_token_from_input('<sample  one = "1"   two=\n"2" />'),
                  get_token_from_input('<sample  one = "1"   two=\n"2" >')]
        for token in tokens:
            self.assertEqual(token.tag, "sample")
            self.assertEqual(len(token.attributes), 2)
            self.assertEqual(token.attributes['one'], '1')
            self.assertEqual(token.attributes['two'], '2')

    def test_trims_whitespaces_in_closing_tag(self):
        tokens = [get_token_from_input('</sample >'),
                  get_token_from_input('</ sample>')]
        for token in tokens:
            self.assertEqual(token.tag, "sample")

    def test_trims_whitespaces_at_beginning(self):
        token = get_token_from_input('  <sample>')
        self._assertOpenTagToken(token, "sample")

    def test_returns_end_of_text_token_at_end(self):
        source = "<sample>"
        lexer = Lexer(source)
        lexer.get_next_token()
        token = lexer.get_next_token()
        self.assertIsInstance(token, EndOfTextToken)

    def test_trims_whitespaces_in_single_tag(self):
        tokens = [get_token_from_input('<sample />'),
                  get_token_from_input('< sample/>')]
        for token in tokens:
            self.assertEqual(token.tag, "sample")

    def test_type_prolog(self):
        token = get_token_from_input('<?xml ?>')
        self.assertIsInstance(token, PrologTagToken)

    def test_tag_prolog(self):
        token = get_token_from_input('<?xml ?>')
        self.assertEqual(token.tag, "xml")

    def test_attributes_prolog(self):
        token = get_token_from_input('<?xml attr="1"  ?>')
        self.assertEqual(len(token.attributes), 1)
        self.assertEqual(token.attributes['attr'], "1")

    def test_recognizes_nested_tag_after_whitespace(self):
        source = "<first> <second>"
        lexer = Lexer(source)
        lexer.get_next_token()
        self._assertOpenTagToken(lexer.get_next_token(), "second")

    def test_recognizes_text_after_whitespace(self):
        source = "<first> second</first>"
        lexer = Lexer(source)
        lexer.get_next_token()
        self._assertTextToken(lexer.get_next_token(), " second")

    def _assertOpenTagToken(self, token, token_tag):
        self.assertIsInstance(token, OpenTagToken)
        self.assertEqual(token.tag, token_tag)

    def _assertCloseTagToken(self, token, token_tag):
        self.assertIsInstance(token, CloseTagToken)
        self.assertEqual(token.tag, token_tag)

    def _assertTextToken(self, token, token_value):
        self.assertIsInstance(token, TextToken)
        self.assertEqual(token.value, token_value)

    def _assertSingleTagToken(self, token, token_tag):
        self.assertIsInstance(token, SingleTagToken)
        self.assertEqual(token.tag, token_tag)


if __name__ == '__main__':
    unittest.main()