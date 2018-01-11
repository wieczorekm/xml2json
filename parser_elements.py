class ParserElement:
    def __init__(self):
        pass


class DocumentTree(ParserElement):
    def __init__(self, xml, prolog):
        super().__init__()
        self.xml = xml
        self.prolog = prolog


class Xml(ParserElement):
    def __init__(self, tag, value, attributes):
        super().__init__()
        self.tag = tag
        self.value = value
        self.attributes = attributes


class BeginOfOpenTag(ParserElement):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag


class Prolog(ParserElement):
    def __init__(self, tag, attributes):
        super().__init__()
        self.tag = tag
        self.attributes = attributes


class CloseTag(ParserElement):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag


class RestOfXml(ParserElement):
    def __init__(self, tag, value):
        super().__init__()
        self.tag = tag
        self.value = value


class Attribute(ParserElement):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value


