class Token:
    def __init__(self):
        pass


class OpenOfTagToken(Token):
    def __init__(self):
        super().__init__()


class OpenOfTagWithSlashToken(Token):
    def __init__(self):
        super().__init__()


class CloseOfTagToken(Token):
    def __init__(self):
        super().__init__()


class CloseOfTagWithSlashToken(Token):
    def __init__(self):
        super().__init__()


class EqualsToken(Token):
    def __init__(self):
        super().__init__()


class IdToken(Token):
    def __init__(self, value):
        super().__init__()
        self.value = value


class QuotedIdToken(Token):
    def __init__(self, value):
        super().__init__()
        self.value = value
