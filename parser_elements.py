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


class Prolog(ParserElement):
    def __init__(self, tag, attributes):
        super().__init__()
        self.tag = tag
        self.attributes = attributes
