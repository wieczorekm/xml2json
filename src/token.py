class Token:
    def __init__(self):
        pass


class TagToken(Token):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag


class AttributeToken(TagToken):
    def __init__(self, tag, attributes):
        super().__init__(tag)
        self.tag = tag
        self.attributes = attributes


class OpenTagToken(AttributeToken):
    def __init__(self, tag, attributes):
        super().__init__(tag, attributes)


class CloseTagToken(TagToken):
    def __init__(self, tag):
        super().__init__(tag)


class TextToken(Token):
    def __init__(self, value):
        super().__init__()
        self.value = value


class SingleTagToken(AttributeToken):
    def __init__(self, tag, attributes):
        super().__init__(tag, attributes)


class EndOfTextToken(Token):
    def __init__(self):
        super().__init__()


class PrologTagToken(AttributeToken):
    def __init__(self, tag, attributes):
        super().__init__(tag, attributes)


class CommentToken(Token):
    def __init__(self, value):
        super().__init__()
        self.value = value
