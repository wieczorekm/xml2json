import unittest
from unittest.mock import Mock

from lexer import Lexer
from parser import *
from parser_elements import DocumentTree
from tokens import *


class ParserTest(unittest.TestCase):

    def test_parses_simple_xml(self):
        lexer = self._create_lexer_mock([OpenTagToken("sample", {}), TextToken("text"), CloseTagToken("sample")])
        parser = Parser(lexer)
        document_tree = parser.get_document_tree()
        self.assertIsInstance(document_tree, DocumentTree)
        self.assertIsNone(document_tree.prolog)
        self.assertEqual(document_tree.xml.tag, "sample")
        self.assertEqual(document_tree.xml.value, "text")

    def test_fails_for_not_matching_tags(self):
        lexer = self._create_lexer_mock([OpenTagToken("sample", {}), TextToken("text"), CloseTagToken("notSample")])
        parser = Parser(lexer)
        # TODO assert message
        self.assertRaises(ParserException, parser.get_document_tree)

    def _create_lexer_mock(self, return_values):
        lexer = Lexer(None)
        lexer.get_next_token = Mock()
        lexer.get_next_token.side_effect = return_values
        return lexer

