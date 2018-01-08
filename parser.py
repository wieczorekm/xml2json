from parser_elements import *
from tokens import *


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer

    def get_document_tree(self):
        first_tag = self.lexer.get_next_token()

        if isinstance(first_tag, OpenTagToken):
            inner_text, inner_xml = self._resolve_xml_inside(first_tag)
            xml = Xml(first_tag.tag, inner_text, first_tag.attributes, [inner_xml])
        else:  # for now it is SingleTag
            xml = Xml(first_tag.tag, None, first_tag.attributes, None)
        return DocumentTree(xml)

    def _resolve_xml_inside(self, first_tag):
        next_tag = self.lexer.get_next_token()
        if isinstance(next_tag, TextToken):
            closetag = self.lexer.get_next_token()
            if first_tag.tag != closetag.tag:
                raise ParserException(
                    "Opentag tag: " + first_tag.tag + " doesn't match closetag tag: " + closetag.tag)
            inner_xml = None
            inner_text = next_tag.value
        elif isinstance(next_tag, OpenTagToken):
            inner_text_tag = self.lexer.get_next_token()
            inner_close_tag = self.lexer.get_next_token()
            outer_close_tag = self.lexer.get_next_token()
            # check inner and outer tags
            inner_xml = Xml(next_tag.tag, inner_text_tag.value, next_tag.attributes, None)
            inner_text = None
        else:  # assuming it is SingleTag
            outer_close_tag = self.lexer.get_next_token()
            # check inner and outer tags
            inner_xml = Xml(next_tag.tag, None, next_tag.attributes, None)
            inner_text = None
        return inner_text, inner_xml


class ParserException(Exception):
    def __init__(self, message):
        super(ParserException, self).__init__()
        self.message = message
