import unittest
import string

from parser_elements import *
from translator import Translator


class TranslatorTest(unittest.TestCase):

    def test_simple_xml(self):
        xml = Xml("xml", "value", None, [])
        document_tree = DocumentTree(xml, None)
        translator = Translator(document_tree)
        json = translator.get_json()
        self.assert_without_whitespaces(json, '{"xml":"value"}')

    def assert_without_whitespaces(self, actual, expected):
        to_remove = str.maketrans('', '', string.whitespace)
        self.assertEqual(actual.translate(to_remove), expected.translate(to_remove))