class ParserElement:
    def __init__(self):
        pass


class DocumentTree(ParserElement):
    def __init__(self, xml):
        super().__init__()
        self.xml = xml


class Xml(ParserElement):
    def __init__(self, id):
        super().__init__()
        self.id = id
