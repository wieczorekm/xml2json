from parser_elements import DocumentTree


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer

    def get_document_tree(self):
        print(self.lexer.get_next_token())
        return DocumentTree()
