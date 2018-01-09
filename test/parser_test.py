import unittest
from unittest.mock import Mock

from lexer import Lexer
from parser import *
from parser_elements import DocumentTree
from tokens import *


class ParserTest(unittest.TestCase):

    def test_parses_simple_xml(self):
        document_tree = self._get_document_tree_from_parser(
            [OpenTagToken("sample", {}), TextToken("text"), CloseTagToken("sample")])
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
        document_tree = self._get_document_tree_from_parser([OpenTagToken("sample", {"one": "1", "two": "2"}),
                                                             TextToken("text"), CloseTagToken("sample")])
        self.assertEqual(document_tree.xml.attributes["one"], "1")
        self.assertEqual(document_tree.xml.attributes["two"], "2")

    def test_works_for_single_tag(self):
        document_tree = self._get_document_tree_from_parser([SingleTagToken("sample", {"one": "1", "two": "2"})])
        self.assertEqual(document_tree.xml.tag, "sample")
        self.assertEqual(document_tree.xml.attributes["one"], "1")
        self.assertEqual(document_tree.xml.attributes["two"], "2")

    def test_works_for_nested_xml(self):
        document_tree = self._get_document_tree_from_parser([OpenTagToken("outer", {"outer": "1"}),
                                                             OpenTagToken("inner", {"inner": "1"}),
                                                             TextToken("text"),
                                                             CloseTagToken("inner"),
                                                             CloseTagToken("outer")])
        self.assertEqual(document_tree.xml.tag, "outer")
        self.assertEqual(document_tree.xml.value, None)
        self.assertEqual(document_tree.xml.attributes["outer"], "1")
        self.assertEqual(document_tree.xml.xmls[0].tag, "inner")
        self.assertEqual(document_tree.xml.xmls[0].attributes["inner"], "1")
        self.assertEqual(document_tree.xml.xmls[0].value, "text")

    def test_works_for_two_layer_nested_xml(self):
        document_tree = self._get_document_tree_from_parser([OpenTagToken("outer", {"outer": "1"}),
                                                             OpenTagToken("middle", {"middle": "1"}),
                                                             OpenTagToken("inner", {"inner": "1"}),
                                                             TextToken("text"),
                                                             CloseTagToken("inner"),
                                                             CloseTagToken("middle"),
                                                             CloseTagToken("outer")])
        self.assertEqual(document_tree.xml.tag, "outer")
        self.assertEqual(document_tree.xml.xmls[0].tag, "middle")
        self.assertEqual(document_tree.xml.xmls[0].xmls[0].tag, "inner")
        self.assertEqual(document_tree.xml.xmls[0].xmls[0].attributes["inner"], "1")
        self.assertEqual(document_tree.xml.xmls[0].xmls[0].value, "text")

    def test_works_for_nested_single_xml_tag(self):
        document_tree = self._get_document_tree_from_parser([OpenTagToken("outer", {"outer": "1"}),
                                                             SingleTagToken("inner", {"inner": "1"}),
                                                             CloseTagToken("outer")])
        self.assertEqual(document_tree.xml.tag, "outer")
        self.assertEqual(document_tree.xml.attributes["outer"], "1")
        self.assertEqual(document_tree.xml.xmls[0].tag, "inner")
        self.assertEqual(document_tree.xml.xmls[0].attributes["inner"], "1")

    def test_works_for_two_nested_single_xmls(self):
        document_tree = self._get_document_tree_from_parser([OpenTagToken("outer", {"outer": "1"}),
                                                             SingleTagToken("inner", {"inner": "1"}),
                                                             SingleTagToken("inner2", {"inner2": "2"}),
                                                             CloseTagToken("outer")])
        self.assertEqual(document_tree.xml.xmls[0].tag, "inner")
        self.assertEqual(document_tree.xml.xmls[0].attributes["inner"], "1")
        self.assertEqual(document_tree.xml.xmls[1].tag, "inner2")
        self.assertEqual(document_tree.xml.xmls[1].attributes["inner2"], "2")

    def test_sample_xml_with_nested_structure(self):
        document_tree = self._get_document_tree_from_parser(
            [OpenTagToken("1", {}), OpenTagToken("2", {}), CloseTagToken("2"), OpenTagToken("3", {}),
             OpenTagToken("4", {}), CloseTagToken("4"), SingleTagToken("5", {}), CloseTagToken("3"),
             CloseTagToken("1")])
        self.assertEqual(document_tree.xml.tag, "1")
        self.assertEqual(document_tree.xml.xmls[0].tag, "2")
        self.assertEqual(document_tree.xml.xmls[1].tag, "3")
        self.assertEqual(document_tree.xml.xmls[1].xmls[0].tag, "4")
        self.assertEqual(document_tree.xml.xmls[1].xmls[1].tag, "5")

    def test_fails_when_there_is_no_eot_when_expected(self):
        lexer = self._create_lexer_mock(
            [OpenTagToken("sample", {}), TextToken("text"), CloseTagToken("sample"), CloseTagToken("sample")])
        parser = Parser(lexer)
        # TODO assert message
        self.assertRaises(ParserException, parser.get_document_tree)

    def _get_document_tree_from_parser(self, tokens):
        lexer = self._create_lexer_mock(tokens)
        parser = Parser(lexer)
        document_tree = parser.get_document_tree()
        return document_tree

    def _create_lexer_mock(self, return_values):
        return_values.append(EndOfTextToken())
        lexer = Lexer(None)
        lexer.get_next_token = Mock()
        lexer.get_next_token.side_effect = return_values
        return lexer
