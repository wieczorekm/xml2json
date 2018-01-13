
class Translator:
    def __init__(self, document_tree):
        self.document_tree = document_tree

    def get_json(self):
        json = '{\n'
        xml = self.document_tree.xml
        json += '\t"' + xml.tag + '"' + ': "' + xml.value + '"\n'
        json += '}'
        return json