class ParserElement:
    def __init__(self):
        pass


class DocumentTree(ParserElement):
    def __init__(self, xml, prolog):
        super().__init__()
        self.xml = xml
        self.prolog = prolog


class Xml(ParserElement):
    def __init__(self, tag, value, attributes, xmls):
        super().__init__()
        self.tag = tag
        self.value = value
        self.attributes = attributes
        self.xmls = xmls


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
    def __init__(self, tag, value, xmls):
        super().__init__()
        self.tag = tag
        self.value = value
        self.xmls = xmls


class Attribute(ParserElement):
    def __init__(self, name, value):
        super().__init__()
        self.name = name
        self.value = value


