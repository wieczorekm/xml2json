from src.parser_elements import *
from src.tokens import *


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def get_document_tree(self):
        self._get_next_token_from_lexer()
        prolog = self._parse_prolog()
        if prolog is not None:
            self._get_next_token_from_lexer()
        xml = self._parse_xml()
        if xml is None:
            self._raise_unexpected_token_error()
        self._get_next_token_from_lexer()
        if not isinstance(self.current_token, EndOfTextToken):
            self._raise_unexpected_token_error()
        return DocumentTree(xml, prolog)

    def _parse_prolog(self):
        if not isinstance(self.current_token, OpenOfPrologTagToken):
            return None
        id = self._get_next_token_from_lexer()
        if not isinstance(self.current_token, IdToken):
            self._raise_unexpected_token_error()
        self._get_next_token_from_lexer()
        casted_attrs = self._parse_multiple_attributes()
        if not isinstance(self.current_token, CloseOfPrologTagToken):
            self._raise_unexpected_token_error()
        return Prolog(id.value, casted_attrs)

    def _parse_xml(self):
        begin_of_open_tag = self._parse_begin_of_open_tag()
        if begin_of_open_tag is None:
            return None
        self._get_next_token_from_lexer()
        casted_attrs = self._parse_multiple_attributes()
        if isinstance(self.current_token, CloseOfTagWithSlashToken):
            return Xml(begin_of_open_tag.tag, None, casted_attrs, [])
        rest_of_xml = self._parse_rest_of_xml()
        if rest_of_xml is None:
            self._raise_unexpected_token_error()
        if begin_of_open_tag.tag != rest_of_xml.tag:
            self._raise_not_equal_ids(begin_of_open_tag, rest_of_xml)
        return Xml(begin_of_open_tag.tag, rest_of_xml.value, casted_attrs, rest_of_xml.xmls)

    def _parse_multiple_attributes(self):
        attribute = self._parse_attr()
        casted_attrs = {}
        while attribute is not None:
            self._get_next_token_from_lexer()
            casted_attrs[attribute.name] = attribute.value
            attribute = self._parse_attr()
        return casted_attrs

    def _parse_rest_of_xml(self):
        if not isinstance(self.current_token, CloseOfTagToken):
            return None
        text, xmls = self._parse_xmls_or_text()
        close_tag = self._parse_close_tag()
        if close_tag is None:
            self._raise_unexpected_token_error()
        return RestOfXml(close_tag.tag, text, xmls)

    def _parse_xmls_or_text(self):
        flag, whitespaces = self.lexer.is_next_nonempty_char_an_open_of_tag()
        text = None
        xmls = []
        if not flag:
            text = self.lexer.get_text_until_open_of_tag()
            text = whitespaces + text
            self._get_next_token_from_lexer()
        else:
            self._get_next_token_from_lexer()
            xml = self._parse_xml()
            while xml is not None:
                xmls.append(xml)
                self._get_next_token_from_lexer()
                xml = self._parse_xml()
        return text, xmls

    def _parse_begin_of_open_tag(self):
        if not isinstance(self.current_token, OpenOfTagToken):
            return None
        id = self._get_next_token_from_lexer()
        if not isinstance(id, IdToken):
            self._raise_unexpected_token_error()
        return BeginOfOpenTag(id.value)

    def _parse_close_tag(self):
        if not isinstance(self.current_token, OpenOfTagWithSlashToken):
            return None
        tag_token = self._get_next_token_from_lexer()
        if not isinstance(self.current_token, IdToken):
            self._raise_unexpected_token_error()
        self._get_next_token_from_lexer()
        if not isinstance(self.current_token, CloseOfTagToken):
            self._raise_unexpected_token_error()
        return CloseTag(tag_token.value)

    def _parse_attr(self):
        if not isinstance(self.current_token, IdToken):
            return None
        id_token = self.current_token
        self._get_next_token_from_lexer()
        if not isinstance(self.current_token, EqualsToken):
            self._raise_unexpected_token_error()
        quoted_token = self._get_next_token_from_lexer()
        if not isinstance(self.current_token, QuotedIdToken):
            self._raise_unexpected_token_error()
        return Attribute(id_token.value, quoted_token.value)

    def _get_next_token_from_lexer(self):
        self.current_token = self.lexer.get_next_token()
        if isinstance(self.current_token, OpenOfCommentTagToken):
            # comments are skipped
            print("[PARSER] Read comment: " + self.lexer.get_comment())
            self.current_token = self.lexer.get_next_token()
            if not isinstance(self.current_token, CloseOfCommentTagToken):
                self._raise_unexpected_token_error()
            self.current_token = self.lexer.get_next_token()
        return self.current_token

    def _raise_not_equal_ids(self, open_id, close_id):
        print("[PARSER] " + open_id.tag + " and " + close_id.tag + " are different near " + str(
            self.lexer.get_current_cursor_pos()))
        raise ParserException("Ids not equal")

    def _raise_unexpected_token_error(self):
        print("[PARSER] Unexpected token near " + str(self.lexer.get_current_cursor_pos()))
        raise ParserException("Unexpected token")


class ParserException(Exception):
    def __init__(self, message):
        super(ParserException, self).__init__()
        self.message = message
