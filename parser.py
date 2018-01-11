from parser_elements import *
from tokens import *


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def get_document_tree(self):
        self._get_next_token_from_lexer()
        # prolog = self._parse_prolog()
        xml = self._parse_xml()
        if xml is None:
            self._raise_unexpected_token_error()
        return DocumentTree(xml)

    # def _parse_prolog(self):
    #     if not isinstance(self.current_token, OpenOfPrologTagToken):
    #         return None
    #     id = self._get_next_token_from_lexer()
    #     if not isinstance(self.current_token, IdToken):
    #         self._raise_unexpected_token_error()
    #     # attrs
    #     self._get_next_token_from_lexer()
    #     if not isinstance(self.current_token, CloseOfPrologTagToken):
    #         self._raise_unexpected_token_error()
    #     self._get_next_token_from_lexer()
    #     return Prolog(id.value)

    def _parse_xml(self):
        begin_of_open_tag = self._parse_begin_of_open_tag()
        if begin_of_open_tag is None:
            return None
        self._get_next_token_from_lexer()
        if isinstance(self.current_token, CloseOfTagWithSlashToken):
            return Xml(begin_of_open_tag.tag, None)
        rest_of_xml = self._parse_rest_of_xml()
        if rest_of_xml is None:
            self._raise_unexpected_token_error()
        if begin_of_open_tag.tag != rest_of_xml.tag:
            print(begin_of_open_tag.tag + " and " + rest_of_xml.tag + " are different")
            self._raise_unexpected_token_error()
        return Xml(begin_of_open_tag.tag, rest_of_xml.value)

    def _parse_rest_of_xml(self):
        if not isinstance(self.current_token, CloseOfTagToken):
            return None
        # only text for now
        flag, whitespaces = self.lexer.is_next_nonempty_char_an_open_of_tag()
        text = None
        if not flag:
            text = self.lexer.get_text_until_open_of_tag()
            text = whitespaces + text
        self._get_next_token_from_lexer()
        close_tag = self._parse_close_tag()
        if close_tag is None:
            self._raise_unexpected_token_error()
        return RestOfXml(close_tag.tag, text)

    def _parse_begin_of_open_tag(self):
        if not isinstance(self.current_token, OpenOfTagToken):
            return None
        id = self._get_next_token_from_lexer()
        if not isinstance(id, IdToken):
            self._raise_unexpected_token_error()
        # attrs
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

    def _get_next_token_from_lexer(self):
        self.current_token = self.lexer.get_next_token()
        return self.current_token

    def _raise_unexpected_token_error(self):
        raise ParserException("Unexpected token")


class ParserException(Exception):
    def __init__(self, message):
        super(ParserException, self).__init__()
        self.message = message
