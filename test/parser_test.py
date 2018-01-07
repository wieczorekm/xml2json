import unittest
from unittest.mock import Mock

from lexer import Lexer
from parser import Parser
from parser_elements import DocumentTree


class ParserTest(unittest.TestCase):

    def test_calls_lexer(self):
        lexer = self._create_lexer_mock(["to_delete"])
        parser = Parser(lexer)
        document_tree = parser.get_document_tree()
        self.assertIsInstance(document_tree, DocumentTree)

    def _create_lexer_mock(self, return_values):
        lexer = Lexer(None)
        lexer.get_next_token = Mock()
        lexer.get_next_token.side_effect = return_values
        return lexer
