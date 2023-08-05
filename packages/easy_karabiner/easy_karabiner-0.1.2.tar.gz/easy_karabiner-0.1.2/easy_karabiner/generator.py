# -*- coding: utf-8 -*-
from collections import OrderedDict
from itertools import groupby
from easy_karabiner import util
from easy_karabiner import __version__
from easy_karabiner.xml_base import XML_base
from easy_karabiner.define import parse_definition
from easy_karabiner.filter import parse_filter
from easy_karabiner.keymap import parse_keymap
from easy_karabiner.lookup import UndefinedFilterException


class Generator(XML_base):
    """
    >>> s1 = Generator().generate()
    >>> s2 = '''
    ...      <root>
    ...        <Easy-Karabiner>{version}</Easy-Karabiner>
    ...        <item>
    ...          <name>Easy-Karabiner</name>
    ...          <item>
    ...            <name>Enable</name>
    ...            <identifier>private.easy_karabiner</identifier>
    ...          </item>
    ...        </item>
    ...      </root>'''.format(version=__version__)
    >>> util.assert_xml_equal(s1, s2)
    """

    ITEM_IDENTIFIER = 'private.easy_karabiner'

    def __init__(self, remaps=[], definitions={}):
        self.remaps = remaps
        self.definitions = definitions

    def init_xml_tree(self):
        version_tag = XML_base.create_tag('Easy-Karabiner', __version__)
        self.xml_tree = XML_base.create_tag('root')
        item_tag = XML_base.create_tag('item')
        self.xml_tree.append(version_tag)
        self.xml_tree.append(item_tag)
        item_tag.append(XML_base.create_tag('name', 'Easy-Karabiner'))
        return item_tag

    def init_subitem_tag(self, item_tag):
        subitem_tag = XML_base.create_tag('item')
        name_tag = XML_base.create_tag('name', 'Enable')
        identifier_tag = XML_base.create_tag('identifier', self.ITEM_IDENTIFIER)
        item_tag.append(subitem_tag)
        subitem_tag.append(name_tag)
        subitem_tag.append(identifier_tag)
        return subitem_tag

    def generate(self):
        item_tag = self.init_xml_tree()

        definitions = self.parse_definitions()
        for d in definitions:
            item_tag.append(d.to_xml())

        blocks = self.parse_remaps()
        subitem_tag = self.init_subitem_tag(item_tag)
        map(lambda block: subitem_tag.append(block.to_xml()), blocks)

        return str(self)

    def parse_definitions(self):
        definitions = []

        for name, vals in self.definitions.items():
            if isinstance(vals, str):
                vals = [vals]
            definition = parse_definition(name, vals)
            definitions.append(definition)

        return definitions

    def parse_remaps(self):
        tmp = OrderedDict()
        filters_table = {}

        for remap in self.remaps:
            keymap, filters = self.parse_remap(remap)
            filters = tuple(filters)
            filters_table[filters] = filters
            tmp.setdefault(filters, []).append(keymap)

        blocks = []
        for filters in tmp:
            keymaps = tmp[filters]
            filters = filters_table[filters]
            block = Block(keymaps, filters)
            blocks.append(block)

        return blocks

    # return (KeyToKey, [Filter])
    def parse_remap(self, remap):
        if not self.is_list_or_tuple(remap) or len(remap) == 0:
            raise Exception('Wrong format')

        if self.is_list_or_tuple(remap[-1]):
            keyargs = remap[:-1]
            try:
                filters = parse_filter(remap[-1])
            except UndefinedFilterException as e:
                print(e)
                exit(1)
        else:
            keyargs = remap
            filters = []

        # I need check if there exist a command item in here
        # otherwise I cannot judge where is the start position of the `keys` args
        if self.is_command_format(keyargs[0]):
            command = self.get_command_value(keyargs.pop(0))
        else:
            command = 'KeyToKey'

        keymap = parse_keymap(command, keyargs)
        return (keymap, filters)

    def is_list_or_tuple(self, obj):
        return isinstance(obj, (list, tuple))

    def is_command_format(self, s):
        return s.startswith('(') and s.endswith(')')

    def get_command_value(self, s):
        return s[1:-1]

    def to_xml(self):
        return self.xml_tree


class Block(XML_base):
    def __init__(self, keymaps, filters=[]):
        self.keymaps = keymaps
        self.filters = filters

    def to_xml(self):
        xml_tree = self.create_tag('block')

        for filter in self.filters:
            xml_tree.append(filter.to_xml())
        for keymap in self.keymaps:
            xml_tree.append(keymap.to_xml())

        return xml_tree


if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'__version__': __version__})
