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

    def test_adds_attributes(self):
        lexer = self._create_lexer_mock([OpenTagToken("sample", {"one": "1", "two": "2"}),
                                         TextToken("text"), CloseTagToken("sample")])
        parser = Parser(lexer)
        document_tree = parser.get_document_tree()
        self.assertEqual(document_tree.xml.attributes["one"], "1")
        self.assertEqual(document_tree.xml.attributes["two"], "2")

    def test_works_for_single_tag(self):
        lexer = self._create_lexer_mock([SingleTagToken("sample", {"one": "1", "two": "2"})])
        parser = Parser(lexer)
        document_tree = parser.get_document_tree()
        self.assertEqual(document_tree.xml.tag, "sample")
        self.assertEqual(document_tree.xml.attributes["one"], "1")
        self.assertEqual(document_tree.xml.attributes["two"], "2")

    def test_works_for_nested_xml(self):
        lexer = self._create_lexer_mock([OpenTagToken("outer", {"outer": "1"}),
                                         OpenTagToken("inner", {"inner": "1"}),
                                         TextToken("text"),
                                         CloseTagToken("inner"),
                                         CloseTagToken("outer")])
        parser = Parser(lexer)
        document_tree = parser.get_document_tree()
        self.assertEqual(document_tree.xml.tag, "outer")
        self.assertEqual(document_tree.xml.value, None)
        self.assertEqual(document_tree.xml.attributes["outer"], "1")
        self.assertEqual(document_tree.xml.xmls[0].tag, "inner")
        self.assertEqual(document_tree.xml.xmls[0].attributes["inner"], "1")
        self.assertEqual(document_tree.xml.xmls[0].value, "text")

    def test_works_for_nested_single_xml_tag(self):
        lexer = self._create_lexer_mock([OpenTagToken("outer", {"outer": "1"}),
                                         SingleTagToken("inner", {"inner": "1"}),
                                         CloseTagToken("outer")])
        parser = Parser(lexer)
        document_tree = parser.get_document_tree()
        self.assertEqual(document_tree.xml.tag, "outer")
        self.assertEqual(document_tree.xml.attributes["outer"], "1")
        self.assertEqual(document_tree.xml.xmls[0].tag, "inner")
        self.assertEqual(document_tree.xml.xmls[0].attributes["inner"], "1")

    def _create_lexer_mock(self, return_values):
        return_values.append(EndOfTextToken())
        lexer = Lexer(None)
        lexer.get_next_token = Mock()
        lexer.get_next_token.side_effect = return_values
        return lexer

