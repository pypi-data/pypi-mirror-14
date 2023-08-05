# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ElementTree
import xmlformatter
from xml.sax.saxutils import unescape


class XML_base(object):
    @staticmethod
    def create_tag(name, text='', **kwargs):
        et = ElementTree.Element(name, **kwargs)
        et.text = text
        return et

    @staticmethod
    def to_format_str(xml_tree):
        formatter = xmlformatter.Formatter()
        rough_string = ElementTree.tostring(xml_tree, 'UTF-8')
        rough_string = unescape(rough_string)
        return formatter.format_string(rough_string)

    @staticmethod
    def parse_file(xml_file):
        return ElementTree.parse(xml_file).getroot()

    def to_xml(self):
        raise Exception('Need override')

    def to_str(self):
        return self.to_format_str(self.to_xml())

    def __str__(self):
        lines = self.to_str().split('\n')
        return '\n'.join(lines[1:])