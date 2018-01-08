class ParserElement:
    def __init__(self):
        pass


class DocumentTree(ParserElement):
    def __init__(self, xml):
        super().__init__()
        self.xml = xml
        self.prolog = None


class Xml(ParserElement):
    def __init__(self, tag, value, attributes, xmls):
        super().__init__()
        self.tag = tag
        self.value = value
        self.attributes = attributes
        self.xmls = xmls
