import unittest
from unittest.mock import Mock

from lexer import Lexer
from parser import *
from tokens import *


class ParserTest(unittest.TestCase):

    def test_parses_single_xml(self):
        document_tree = self._get_document_tree_from_parser(
            [OpenOfTagToken(), IdToken("xml"), CloseOfTagWithSlashToken()])
        self.assertEqual(document_tree.xml.tag, "xml")

    def test_parses_xml_with_text(self):
        document_tree = self._get_document_tree_from_parser(
            [OpenOfTagToken(), IdToken("xml"), CloseOfTagToken(), OpenOfTagWithSlashToken(), IdToken("xml"),
             CloseOfTagToken()])
        self.assertEqual(document_tree.xml.tag, "xml")
        self.assertEqual(document_tree.xml.value, "text")

    def test_parses_single_xml_with_comment(self):
        document_tree = self._get_document_tree_from_parser(
            [OpenOfCommentTagToken(), CloseOfCommentTagToken(), OpenOfTagToken(), IdToken("xml"),
             CloseOfTagWithSlashToken()])
        self.assertEqual(document_tree.xml.tag, "xml")

    def test_parses_single_xml_with_prolog(self):
        document_tree = self._get_document_tree_from_parser(
            [OpenOfPrologTagToken(), IdToken("prolog"), IdToken("attr"), EqualsToken(), QuotedIdToken("1"),
             IdToken("attr2"), EqualsToken(), QuotedIdToken("2"), CloseOfPrologTagToken(), OpenOfTagToken(),
             IdToken("xml"),
             CloseOfTagWithSlashToken()])
        self.assertEqual(document_tree.prolog.tag, "prolog")
        self.assertEqual(document_tree.xml.tag, "xml")
        self.assertEqual(document_tree.prolog.attributes["attr"], "1")
        self.assertEqual(document_tree.prolog.attributes["attr2"], "2")

    def test_parses_single_xml_with_attr(self):
        document_tree = self._get_document_tree_from_parser(
            [OpenOfTagToken(), IdToken("xml"), IdToken("attr"), EqualsToken(), QuotedIdToken("1"), IdToken("attr2"),
             EqualsToken(), QuotedIdToken("2"), CloseOfTagWithSlashToken()])
        self.assertEqual(document_tree.xml.tag, "xml")
        self.assertEqual(document_tree.xml.attributes["attr"], "1")
        self.assertEqual(document_tree.xml.attributes["attr2"], "2")

    def _get_document_tree_from_parser(self, return_values):
        lexer = self._create_lexer_mock(return_values)
        parser = Parser(lexer)
        document_tree = parser.get_document_tree()
        return document_tree

    def _create_lexer_mock(self, return_values):
        # return_values.append(EndOfTextToken())
        lexer = Lexer(None)
        lexer.get_next_token = Mock()
        lexer.is_next_nonempty_char_an_open_of_tag = Mock()
        lexer.get_text_until_open_of_tag = Mock()
        lexer.get_comment = Mock()
        lexer.get_next_token.side_effect = return_values
        lexer.is_next_nonempty_char_an_open_of_tag.side_effect = [(False, "")]
        lexer.get_text_until_open_of_tag.side_effect = ["text"]
        lexer.get_comment.side_effect = ["comment"]
        return lexer
