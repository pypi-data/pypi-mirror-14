# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import OrderedDict
from easy_karabiner import __version__
from easy_karabiner import exception
from easy_karabiner.xml_base import XML_base
from easy_karabiner.define import parse_definition
from easy_karabiner.filter import parse_filter
from easy_karabiner.keymap import parse_keymap


class Generator(XML_base):
    """
    >>> from easy_karabiner import util
    >>> g = Generator()
    >>> s = '''
    ...     <root>
    ...       <Easy-Karabiner>{version}</Easy-Karabiner>
    ...       <item>
    ...         <name>Easy-Karabiner</name>
    ...         <item>
    ...           <name>Enable</name>
    ...           <identifier>private.easy_karabiner</identifier>
    ...         </item>
    ...       </item>
    ...     </root>'''.format(version=__version__)
    >>> util.assert_xml_equal(g, s)
    """

    ITEM_IDENTIFIER = 'private.easy_karabiner'

    def __init__(self, remaps=None, definitions=None):
        self.remaps = remaps or []
        self.definitions = definitions or {}
        self.xml_tree = None

    def init_xml_tree(self, xml_root):
        version_tag = XML_base.create_tag('Easy-Karabiner', __version__)
        item_tag = XML_base.create_tag('item')
        item_tag.append(XML_base.create_tag('name', 'Easy-Karabiner'))
        xml_root.append(version_tag)
        xml_root.append(item_tag)
        return item_tag

    def init_subitem_tag(self, item_tag):
        subitem_tag = XML_base.create_tag('item')
        name_tag = XML_base.create_tag('name', 'Enable')
        identifier_tag = XML_base.create_tag('identifier', self.ITEM_IDENTIFIER)
        item_tag.append(subitem_tag)
        subitem_tag.append(name_tag)
        subitem_tag.append(identifier_tag)
        return subitem_tag

    def to_xml(self):
        if self.xml_tree is None:
            self.xml_tree = XML_base.create_tag('root')
            definitions = self.parse_definitions(self.definitions)
            blocks = self.parse_remaps(self.remaps)

            # construct XML tree
            item_tag = self.init_xml_tree(self.xml_tree)
            for d in definitions:
                item_tag.append(d.to_xml())
            subitem_tag = self.init_subitem_tag(item_tag)
            for block in blocks:
                subitem_tag.append(block.to_xml())

        return self.xml_tree

    def parse_definitions(self, definitions):
        defs = []

        for name in sorted(definitions.keys()):
            vals = definitions[name]
            if not self.is_list_or_tuple(vals):
                vals = [vals]

            try:
                definition = parse_definition(name, vals)
                defs.append(definition)
            except exception.UnsupportDefinitionType as e:
                errmsg = "Invalid definition:\n\t%s" % e
                raise exception.UnsupportDefinitionType(errmsg)

        return defs

    def parse_remaps(self, remaps):
        # used for grouping keymap by filters
        filters_keymaps_tbl = OrderedDict()

        for remap in remaps:
            if self.is_list_or_tuple(remap) and len(remap) > 0:
                keymap, filters = self.parse_remap(remap)
                filters_keymaps_tbl.setdefault(filters, []).append(keymap)
            else:
                errmsg = 'Remap must be a list or tuple:\n\t%s' % remap.__repr__()
                raise exception.ConfigError(errmsg)

        blocks = []
        for filters in filters_keymaps_tbl:
            keymaps = filters_keymaps_tbl[filters]
            blocks.append(Block(keymaps, filters))

        return blocks

    # return (KeyToKey, [Filter])
    def parse_remap(self, remap):
        # last element in remap is [Filter]?
        if self.is_list_or_tuple(remap[-1]):
            keyargs = remap[:-1]
            try:
                filters = parse_filter(remap[-1])
            except exception.UndefinedFilterException as e:
                errmsg = "Undefined filters:\n\t%s" % e
                raise exception.UnsupportDefinitionType(errmsg)
        else:
            keyargs = remap
            filters = []

        # first element is remap type indicator?
        if self.is_command_format(keyargs[0]):
            command = self.get_command_value(keyargs.pop(0))
        else:
            command = 'KeyToKey'

        keymap = parse_keymap(command, keyargs)

        return (keymap, tuple(filters))

    def is_list_or_tuple(self, obj):
        return isinstance(obj, (list, tuple))

    def is_command_format(self, s):
        return s.startswith('(') and s.endswith(')')

    def get_command_value(self, s):
        return s[1:-1]


class Block(XML_base):
    def __init__(self, keymaps, filters=None):
        self.keymaps = keymaps
        self.filters = filters or tuple()

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