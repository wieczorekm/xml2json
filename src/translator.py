class Translator:
    def __init__(self, document_tree, config):
        self.document_tree = document_tree
        self.copy_attributes = config['copy_attributes'] if 'copy_attributes' in config else True
        self.attribute_prefix = config['attribute_prefix'] if 'attribute_prefix' in config else "attr-"
        self.text_name = config['text_name'] if 'text_name' in config else "#text"

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

            xmls = {}
            for loop_xml in xml.xmls:
                if loop_xml.tag not in xmls.keys():
                    xmls[loop_xml.tag] = [loop_xml]
                else:
                    xmls[loop_xml.tag].append(loop_xml)

            counter = 0
            for key, loop_xmls in sorted(xmls.items()):
                if len(loop_xmls) == 1:
                    loop_xml = loop_xmls[0]
                    inner += "\t" * nest_level
                    inner += '"' + loop_xml.tag + '": ' + self.translate_xml(loop_xml, nest_level + 1)
                    inner += '\n' if counter == len(xml.xmls) - 1 else ',\n'
                    counter += 1
                else:
                    inner += "\t" * nest_level
                    inner += '"' + loop_xmls[0].tag + '": [\n'
                    loop_counter = 0
                    for loop_xml in loop_xmls:
                        inner += "\t" * (nest_level + 1)
                        inner += self.translate_xml(loop_xml, nest_level + 2)
                        if loop_counter != len(loop_xmls) - 1:
                            inner += ",\n"
                        counter += 1
                        loop_counter += 1
                    inner += '\n'
                    inner += "\t" * nest_level + "]"
                    inner += '\n' if counter == len(xml.xmls) else ',\n'

            inner += "\t" * (nest_level - 1)
            inner += '}'
            return inner
        else:
            return self.get_xml_value(xml.value) if not xml.attributes else self.translate_body_with_attributes(xml, nest_level)

    def translate_body_with_attributes(self, xml, nest_level):
        body = '{\n'
        if self.copy_attributes:
            for attr in sorted(xml.attributes):
                body += "\t" * nest_level
                body += '"' + self.attribute_prefix + attr + '": "' + xml.attributes[attr] + '",\n'
        body += "\t" * nest_level
        body += '"' + self.text_name + '":' + self.get_xml_value(xml.value) + '\n'
        body += "\t" * (nest_level - 1)
        body += '}'
        return body

    def translate_prolog(self, prolog):
        prolog_as_string = '\t"prolog":{\n'
        for idx, attr in enumerate(sorted(prolog.attributes)):
            prolog_as_string += '\t\t"' + attr + '": "' + prolog.attributes[attr]
            prolog_as_string += '"\n' if idx == len(prolog.attributes) - 1 else '",\n'
        prolog_as_string += "\t},\n"
        return prolog_as_string

    def get_xml_value(self, value):
        return '"' + value + '"' if value else "null"
