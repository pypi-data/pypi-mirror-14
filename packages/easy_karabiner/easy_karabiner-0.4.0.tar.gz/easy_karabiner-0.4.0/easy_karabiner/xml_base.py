# -*- coding: utf-8 -*-
import lxml.etree as etree
import xml.dom.minidom as minidom
from easy_karabiner import exception


class XML_base(object):
    @staticmethod
    def parse(filepath):
        return etree.parse(filepath).getroot()

    @staticmethod
    def parse_string(xml_str):
        return etree.fromstring(xml_str)

    def get_clsname(self):
        return self.__class__.__name__

    @staticmethod
    def create_cdata_text(text):
        return etree.CDATA(text)

    @staticmethod
    def create_tag(name, text=None, **kwargs):
        et = etree.Element(name, **kwargs)
        et.text = text
        return et

    @staticmethod
    def pretty_text(elem, indent="  ", level=0):
        i = "\n" + level * indent

        if len(elem) == 0:
            if elem.text is not None:
                lines = elem.text.split('\n')
                if len(lines) > 1:
                    if not lines[0].startswith(' '):
                        lines[0] = (i + indent) + lines[0]
                    if lines[-1].strip() == '':
                        lines.pop()
                    elem.text = (i + indent).join(lines) + i
        else:
            for subelem in elem:
                XML_base.pretty_text(subelem, indent, level + 1)

        return elem

    @staticmethod
    def to_format_str(xml_tree, pretty_text=True):
        indent = "  "
        if pretty_text:
            XML_base.pretty_text(xml_tree, indent=indent)
        xml_string = etree.tostring(xml_tree)
        xml_string = minidom.parseString(xml_string).toprettyxml(indent=indent)
        return xml_string

    def to_xml(self):
        raise exception.NeedOverrideError()

    def to_str(self, pretty_text=True, remove_first_line=False):
        xml_str = self.to_format_str(self.to_xml(), pretty_text=pretty_text)

        if remove_first_line:
            lines = xml_str.split('\n')[1:]
            return '\n'.join(lines)
        else:
            return xml_str

    def __str__(self):
        # remove version tag
        return self.to_str(remove_first_line=True)