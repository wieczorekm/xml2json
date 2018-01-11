import unittest

from lexer import Lexer
from tokens import *


def get_token_from_input(source):
    lexer = Lexer(source)
    token = lexer.get_next_token()
    return token


class LexerTest(unittest.TestCase):

    def test_open_token(self):
        token = get_token_from_input("<")
        self.assertIsInstance(token, OpenOfTagToken)

    def test_open_of_single_tag(self):
        token = get_token_from_input("</")
        self.assertIsInstance(token, OpenOfTagWithSlashToken)

    def test_close_of_tag(self):
        token = get_token_from_input("/>")
        self.assertIsInstance(token, CloseOfTagWithSlashToken)

    def test_close_of_single_tag(self):
        token = get_token_from_input(">")
        self.assertIsInstance(token, CloseOfTagToken)

    def test_equals_tag(self):
        token = get_token_from_input("=")
        self.assertIsInstance(token, EqualsToken)

    def test_id_tag(self):
        token = get_token_from_input("xml ")
        self.assertIsInstance(token, IdToken)
        self.assertEqual(token.value, "xml")

    def test_open_tag(self):
        lexer = Lexer("<tag>")
        open_token = lexer.get_next_token()
        id = lexer.get_next_token()
        close_token = lexer.get_next_token()
        self.assertIsInstance(open_token, OpenOfTagToken)
        self.assertIsInstance(id, IdToken)
        self.assertEqual(id.value, "tag")
        self.assertIsInstance(close_token, CloseOfTagToken)

    def test_close_tag(self):
        lexer = Lexer("<tag/>")
        open_token = lexer.get_next_token()
        id = lexer.get_next_token()
        close_token = lexer.get_next_token()
        self.assertIsInstance(open_token, OpenOfTagToken)
        self.assertIsInstance(id, IdToken)
        self.assertEqual(id.value, "tag")
        self.assertIsInstance(close_token, CloseOfTagWithSlashToken)

    def test_with_spaces(self):
        lexer = Lexer("  </   tag  >  ")
        open_token = lexer.get_next_token()
        id = lexer.get_next_token()
        close_token = lexer.get_next_token()
        self.assertIsInstance(open_token, OpenOfTagWithSlashToken)
        self.assertIsInstance(id, IdToken)
        self.assertEqual(id.value, "tag")
        self.assertIsInstance(close_token, CloseOfTagToken)

    def test_tag_with_attr(self):
        lexer = Lexer('<tag a="1"/>')
        self.assertIsInstance(lexer.get_next_token(), OpenOfTagToken)
        tag = lexer.get_next_token()
        self.assertIsInstance(tag, IdToken)
        self.assertEqual(tag.value, "tag")
        attr = lexer.get_next_token()
        self.assertIsInstance(attr, IdToken)
        self.assertEqual(attr.value, "a")
        self.assertIsInstance(lexer.get_next_token(), EqualsToken)
        attr_value = lexer.get_next_token()
        self.assertIsInstance(attr_value, QuotedIdToken)
        self.assertEqual(attr_value.value, "1")
        self.assertIsInstance(lexer.get_next_token(), CloseOfTagWithSlashToken)

    def test_end_of_text_token(self):
        lexer = Lexer("<")
        lexer.get_next_token()
        end_of_text_token = lexer.get_next_token()
        self.assertIsInstance(end_of_text_token, EndOfTextToken)

    def test_get_string_method(self):
        lexer = Lexer("> text <")
        self.assertIsInstance(lexer.get_next_token(), CloseOfTagToken)
        text = lexer.get_text_until_open_of_tag()
        self.assertEqual(text, " text ")
        self.assertIsInstance(lexer.get_next_token(), OpenOfTagToken)

    def test_check_whitespace_method_with_text(self):
        lexer = Lexer("> text <")
        self.assertIsInstance(lexer.get_next_token(), CloseOfTagToken)
        flag, buffer = lexer.is_next_nonempty_char_an_open_of_tag()
        self.assertEqual(flag, False)
        self.assertEqual(buffer, " ")

    def test_check_whitespace_method_without_text(self):
        lexer = Lexer("> <")
        self.assertIsInstance(lexer.get_next_token(), CloseOfTagToken)
        flag, buffer = lexer.is_next_nonempty_char_an_open_of_tag()
        self.assertEqual(flag, True)
        self.assertIsInstance(lexer.get_next_token(), OpenOfTagToken)

    def test_prolog_open_token(self):
        token = get_token_from_input("<?")
        self.assertIsInstance(token, OpenOfPrologTagToken)

    def test_prolog_close_token(self):
        token = get_token_from_input("?>")
        self.assertIsInstance(token, CloseOfPrologTagToken)

    def test_comment_open_token(self):
        token = get_token_from_input("<!--")
        self.assertIsInstance(token, OpenOfCommentTagToken)

    def test_get_comment_method(self):
        lexer = Lexer("<!-- comment --> <")
        self.assertIsInstance(lexer.get_next_token(), OpenOfCommentTagToken)
        self.assertEqual(lexer.get_comment(), " comment ")
        self.assertIsInstance(lexer.get_next_token(), CloseOfCommentTagToken)
        self.assertIsInstance(lexer.get_next_token(), OpenOfTagToken)

    def test_get_single_quoted_id(self):
        lexer = Lexer("\'id\'")
        token = lexer.get_next_token()
        self.assertIsInstance(token, QuotedIdToken)
        self.assertEqual(token.value, "id")

if __name__ == '__main__':
    unittest.main()
