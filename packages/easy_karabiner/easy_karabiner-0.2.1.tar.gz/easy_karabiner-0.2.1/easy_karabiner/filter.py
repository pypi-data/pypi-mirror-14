# -*- coding: utf-8 -*-
from __future__ import print_function
from functools import reduce
from itertools import groupby
from easy_karabiner import util
from easy_karabiner.lookup import DefQuery
from easy_karabiner.xml_base import XML_base


class BaseFilter(XML_base, util.Hashable):
    def __init__(self, *vals, **kwargs):
        self.type = kwargs.get('type', 'only')
        self.vals = vals
        self.kwargs = kwargs

    def get_vals(self):
        return self.vals

    def get_tag_name(self):
        header = self.__class__.__name__.lower().rsplit('filter', 1)[0]
        tag_name = '%s_%s' % (header, self.type)
        return tag_name

    def to_xml(self):
        xml_tree = self.create_tag(self.get_tag_name())
        xml_tree.text = ',\n'.join(self.get_vals())
        return xml_tree

    def __add__(self, another):
        if self.get_tag_name() == another.get_tag_name():
            self.vals += another.vals
            return self
        else:
            msg = "Can't add %s with %s" % (self.get_tag_name(), another.get_tag_name())
            raise Exception(msg)

    def _id(self):
        return (self.get_tag_name(), tuple(self.get_vals()))


class Filter(BaseFilter):
    '''
    >>> print(Filter('SKIM'))
    <only>SKIM</only>
    >>> print(Filter('SKIM', type='not'))
    <not>SKIM</not>
    '''

    def get_tag_name(self):
        return self.type


class ReplacementFilter(Filter):
    pass


class DeviceFilter(BaseFilter):
    def get_tag_name(self):
        tag_name = 'device_%s' % self.type
        return tag_name


class DeviceProductFilter(DeviceFilter):
    pass


class DeviceVendorFilter(DeviceFilter):
    pass


class WindowNameFilter(BaseFilter):
    pass


class UIElementRoleFilter(BaseFilter):
    pass


class InputSourceFilter(BaseFilter):
    pass


_CLASSES = util.find_all_subclass_of(BaseFilter, globals())

def split_type_and_val(val):
    if val.startswith('!'):
        type = 'not'
        val = val[1:]
    else:
        type = 'only'

    if val.startswith('{{') and val.endswith('}}'):
        val = val[2:-2]

    return (type, val)

# @return [Filter]
def parse_filter(vals):
    type_val_pairs = map(split_type_and_val, vals)

    # create filters
    filters = []
    for type, val in type_val_pairs:
        clsname = DefQuery.query_filter(val) or 'Filter'

        if clsname == 'ReplacementFilter':
            val = '{{%s}}' % val
        elif clsname == 'DeviceProductFilter':
            val = 'DeviceProduct::%s' % val
        elif clsname == 'DeviceVendorFilter':
            val = 'DeviceVendor::%s' % val

        for cls in _CLASSES:
            if clsname == cls.__name__:
                filter = cls(val, type=type)
                filters.append(filter)
                break

    filters_lists = [list(v) for k, v in groupby(filters, lambda f: f.get_tag_name())]
    filters = list(map(lambda fs: reduce(lambda x, y: x + y, fs), filters_lists))
    return filters


if __name__ == "__main__":
    import doctest
    doctest.testmod()