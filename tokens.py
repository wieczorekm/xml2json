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

    def __str__(self):
        return "[OpenTagToken] " + self.tag + str(self.attributes)


class CloseTagToken(TagToken):
    def __init__(self, tag):
        super().__init__(tag)

    def __str__(self):
        return "[CloseTagToken] " + self.tag


class TextToken(Token):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return "[TextToken] " + self.value


class SingleTagToken(AttributeToken):
    def __init__(self, tag, attributes):
        super().__init__(tag, attributes)

    def __str__(self):
        return "[SingleTagToken] " + self.tag + str(self.attributes)


class EndOfTextToken(Token):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "[EndOfTextToken]"


class PrologTagToken(AttributeToken):
    def __init__(self, tag, attributes):
        super().__init__(tag, attributes)

    def __str__(self):
        return "[PrologTagToken] " + self.tag + str(self.attributes)


class CommentToken(Token):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return "[CommentToken] " + self.value
