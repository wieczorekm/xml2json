
class Translator:
    def __init__(self, document_tree):
        self.document_tree = document_tree

    def get_json(self):
        json = '{\n'
        xml = self.document_tree.xml
        json += '\t"' + xml.tag + '":' + self.translate_xml(xml)
        json += '}'
        return json

    def translate_xml(self, xml):
        if len(xml.xmls) > 0:
            inner = '{\n'
            for idx, loop_xml in enumerate(xml.xmls):
                inner += '\t"' + loop_xml.tag + '": ' + self.translate_xml(loop_xml)
                inner += '\n' if idx == len(xml.xmls) - 1 else ',\n'
            inner += '}\n'
            return inner
        else:
            return self.translate_body(xml)

    def translate_body(self, xml):
        return '"' + xml.value + '"\n' if not xml.attributes else self.translate_body_with_attributes(xml)

    def translate_body_with_attributes(self, xml):
        body = '{\n'
        for attr in sorted(xml.attributes):
            body += '\t"attr-' + attr + '": "' + xml.attributes[attr] + '",\n'
        body += '"#text": "' + xml.value + '"\n'
        body += '}\n'
        return body
