class ParserElement:
    def __init__(self):
        pass


class DocumentTree(ParserElement):
    def __init__(self, xml, prolog):
        super().__init__()
        self.xml = xml
        self.prolog = prolog


class Xml(ParserElement):
    def __init__(self, tag, value):
        super().__init__()
        self.tag = tag
        self.value = value


class BeginOfOpenTag(ParserElement):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag


class Prolog(ParserElement):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag


class CloseTag(ParserElement):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag


class RestOfXml(ParserElement):
    def __init__(self, tag, value):
        super().__init__()
        self.tag = tag
        self.value = value
