import string
import unittest

from json import loads
from src.parser_elements import *
from src.translator import Translator


class TranslatorTest(unittest.TestCase):

    def test_simple_xml(self):
        xml = Xml("xml", "value", None, [])
        self.assert_without_whitespaces(self.get_json_from_translator(xml), '{"xml":"value"}')

    def test_nested_xml(self):
        inner_xmls = [Xml("inner1", "value1", None, []), Xml("inner2", "value2", None, [])]
        xml = Xml("outer", None, None, inner_xmls)
        self.assert_without_whitespaces(self.get_json_from_translator(xml),
                                        ''' {
                                                "outer":{
                                                    "inner1":"value1",
                                                    "inner2":"value2"
                                                }
                                            }''')

    def test_double_nested(self):
        inner = Xml("inner", "value", None, [])
        middle = Xml("middle", None, None, [inner])
        outer = Xml("outer", None, None, [middle])
        self.assert_without_whitespaces(self.get_json_from_translator(outer),
                                        ''' {
                                                "outer":{
                                                    "middle": {
                                                        "inner": "value"
                                                    }
                                                }
                                            }''')

    def test_with_attributes(self):
        xml = Xml("xml", "value", {"1": "val1", "2": "val2"}, [])
        self.assert_without_whitespaces(self.get_json_from_translator(xml),
                                        ''' {
                                            "xml":{
                                                "attr-1":"val1",
                                                "attr-2":"val2",
                                                "#text":"value"
                                            }
                                        }''')

    def test_with_prolog(self):
        prolog = Prolog("xml", {"1": "val1", "2": "val2"})
        xml = Xml("xml", "value", None, [])
        self.assert_without_whitespaces(self.get_json_from_translator(xml, prolog),
                                        ''' {
                                            "prolog":{
                                                "1": "val1",
                                                "2": "val2"
                                            },
                                            "xml": "value"
                                        }''')


    def get_json_from_translator(self, xml, prolog=None):
        document_tree = DocumentTree(xml, prolog)
        translator = Translator(document_tree, loads('{}'))
        json = translator.get_json()
        return json

    def assert_without_whitespaces(self, actual, expected):
        to_remove = str.maketrans('', '', string.whitespace)
        self.assertEqual(actual.translate(to_remove), expected.translate(to_remove))
