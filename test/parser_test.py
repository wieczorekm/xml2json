import unittest
from unittest.mock import Mock

from lexer import Lexer
from parser import *
from tokens import *


class ParserTest(unittest.TestCase):

    def test_parses_single_xml(self):
        lexer = self._create_lexer_mock([OpenOfTagToken, IdToken("xml"), CloseOfTagWithSlashToken])
        parser = Parser(lexer)
        document_tree = parser.get_document_tree()
        self.assertEqual(document_tree.xml.id, "xml")


    def _create_lexer_mock(self, return_values):
        # return_values.append(EndOfTextToken())
        lexer = Lexer(None)
        lexer.get_next_token = Mock()
        lexer.get_next_token.side_effect = return_values
        return lexer
