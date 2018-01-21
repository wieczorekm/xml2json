class Translator:
    def __init__(self, document_tree):
        self.document_tree = document_tree

    def get_json(self):
        json = '{\n'
        prolog = self.document_tree.prolog
        json += self.translate_prolog(prolog) if prolog else ""
        xml = self.document_tree.xml
        json += '\t"' + xml.tag + '":' + self.translate_xml(xml, 2)
        json += '\n}'
        return json

    def translate_xml(self, xml, nest_level):
        if len(xml.xmls) > 0:
            inner = '{\n'
            for idx, loop_xml in enumerate(xml.xmls):
                inner += "\t" * nest_level
                inner += '"' + loop_xml.tag + '": ' + self.translate_xml(loop_xml, nest_level + 1)
                inner += '\n' if idx == len(xml.xmls) - 1 else ',\n'
            inner += "\t" * (nest_level - 1)
            inner += '}'
            return inner
        else:
            return self.get_xml_value(xml.value) if not xml.attributes else self.translate_body_with_attributes(xml, nest_level)

    def translate_body_with_attributes(self, xml, nest_level):
        body = '{\n'
        for attr in sorted(xml.attributes):
            body += "\t" * nest_level
            body += '"attr-' + attr + '": "' + xml.attributes[attr] + '",\n'
        body += "\t" * nest_level
        body += '"#text":' + self.get_xml_value(xml.value) + '\n'
        body += "\t" * (nest_level - 1)
        body += '}'
        return body

    def translate_prolog(self, prolog):
        prolog_as_string = '\t"prolog":{\n'
        for idx, attr in enumerate(sorted(prolog.attributes)):
            prolog_as_string += '\t\t"' + attr + '": "' + prolog.attributes[attr]
            prolog_as_string += '"\n' if idx == len(prolog.attributes) - 1 else '\",\n'
        prolog_as_string += "\t},\n"
        return prolog_as_string

    def get_xml_value(self, value):
        return '"' + value + '"' if value else "null"
