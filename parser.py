from parser_elements import *
from tokens import *


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer

    def get_document_tree(self):
        first_tag = self.lexer.get_next_token()

        if isinstance(first_tag, OpenTagToken):
            next_tag = self.lexer.get_next_token()
            inner_text, inner_xmls, close_tag = self._resolve_xml_inside(next_tag)
            self._validate_tags(first_tag, close_tag)
            xml = Xml(first_tag.tag, inner_text, first_tag.attributes, inner_xmls)
        else:  # for now it is SingleTag
            xml = Xml(first_tag.tag, None, first_tag.attributes, [])
        return DocumentTree(xml)

    def _resolve_xml_inside(self, next_tag):
        if isinstance(next_tag, TextToken):
            return next_tag.value, None, self.lexer.get_next_token()
        xmls, close_tag = self._resolve_xml_array(next_tag)
        return None, xmls, close_tag

    def _resolve_xml_array(self, next_tag):
        xmls = []
        while isinstance(next_tag, OpenTagToken) or isinstance(next_tag, SingleTagToken):
            if isinstance(next_tag, SingleTagToken):
                xmls.append(Xml(next_tag.tag, None, next_tag.attributes, []))
                next_tag = self.lexer.get_next_token()
            else:  # assuming that this is OpenTag
                inner_next_tag = self.lexer.get_next_token()
                if isinstance(inner_next_tag, TextToken):
                    inner_close_tag = self.lexer.get_next_token()  # assuming this is CloseTag
                    self._validate_tags(next_tag, inner_close_tag)
                    xmls.append(Xml(next_tag.tag, inner_next_tag.value, next_tag.attributes, []))
                else: # assuming that this is OpenTag
                    open_tag = next_tag
                    inner_text, inner_xmls, next_tag = self._resolve_xml_inside(inner_next_tag)
                    self._validate_tags(open_tag, next_tag)
                    xmls.append(Xml(open_tag.tag, inner_text, open_tag.attributes, inner_xmls))
                next_tag = self.lexer.get_next_token()
        return xmls, next_tag

    def _validate_tags(self, first_tag, close_tag):
        if first_tag.tag != close_tag.tag:
            raise ParserException(
                "Opentag tag: " + first_tag.tag + " doesn't match closetag tag: " + close_tag.tag)


class ParserException(Exception):
    def __init__(self, message):
        super(ParserException, self).__init__()
        self.message = message
