class Token:
    def __init__(self):
        pass


class OpenTagToken(Token):
    def __init__(self, tag, attributes):
        super().__init__()
        self.tag = tag
        self.attributes = attributes


class CloseTagToken(Token):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag


class TextToken(Token):
    def __init__(self, value):
        super().__init__()
        self.value = value