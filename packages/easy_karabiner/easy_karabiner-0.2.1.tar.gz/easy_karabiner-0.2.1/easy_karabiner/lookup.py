# -*- coding: utf-8 -*-
from __future__ import print_function

import os
from easy_karabiner import alias
from easy_karabiner.xml_base import XML_base
from easy_karabiner.def_filter_map import get_name_tag_by_def_tag, get_filter_by_def

# alias is case-insensitive
def _get_alias(tblname, k, d=None):
    return alias.__dict__[tblname].get(k.lower(), k if d is None else d)

def _update_alias(tblname, aliases):
    alias.__dict__[tblname].update(aliases)

def get_key_alias(k, d=None):
    return _get_alias('KEY_ALIAS', k, d)

def get_def_alias(k, d=None):
    return _get_alias('DEF_ALIAS', k, d)

def get_keymap_alias(k, d=None):
    return _get_alias('KEYMAP_ALIAS', k, d)

def update_key_alias(aliases):
    _update_alias('KEY_ALIAS', aliases)

def update_def_alias(aliases):
    _update_alias('DEF_ALIAS', aliases)

def update_keymap_alias(aliases):
    _update_alias('KEYMAP_ALIAS', aliases)


class BaseQuery(object):
    # NOTICE: need override
    DATA_DIR = None
    DATA_SUFFIX = None
    QUERY_ORDER = None

    def __init__(self):
        self.data = {}

    @classmethod
    def get_instance(cls):
        if hasattr(cls, '_instance'):
            return cls._instance
        else:
            cls._instance = cls()
            cls._instance.load_data()
            return cls._instance

    @classmethod
    def query(cls, value):
        for k in cls.QUERY_ORDER:
            if cls.is_in(k, value):
                return k
        return None

    @classmethod
    def is_in(cls, k, value):
        if value in cls.get_instance().get(k, []):
            return k
        else:
            return None

    def get(self, k, default=None):
        return self.data.get(k, default or [])

    def load_data(self):
        for type in self.QUERY_ORDER:
            self.data[type] = set(self.get_data(type))
        return self

    def get_datapath(self, type):
        basename = '%s.%s' % (type, self.DATA_SUFFIX)
        return os.path.join(os.path.dirname(__file__), self.DATA_DIR, basename)

    def get_data(self, type):
        raise Exception("Need override")


# Data file come from https://github.com/tekezo/Karabiner/tree/master/src/bridge/generator/keycode/data
class KeyCodeQuery(BaseQuery):
    ''' Query header of key

    >>> print(KeyCodeQuery.query('A'))
    KeyCode

    >>> print(KeyCodeQuery.query('NOREPEAT'))
    Option
    '''

    DATA_DIR = 'data/keycode'
    DATA_SUFFIX = 'data'

    QUERY_ORDER = ['ModifierFlag',
                   'ConsumerKeyCode',
                   'KeyCode',
                   'Option',
                   'InputSource',
                   'PointingButton',
                   'DeviceProduct',
                   'DeviceVendor',
                   'KeyboardType',]


    def get_data(self, type):
        data = []

        with open(self.get_datapath(type), 'r') as fp:
            lines = fp.readlines()
            # remove comment line and whitespace line
            lines = filter(lambda l: not l.startswith('//') and not l.isspace(), lines)
            lines = map(lambda l: l.strip(), lines)
            data = list(map(lambda l: l.split()[0], lines))

        return data


class UndefinedFilterException(Exception):
    pass


# Data file come from https://github.com/tekezo/Karabiner/tree/master/src/core/server/Resources/
class DefQuery(BaseQuery):
    ''' Query definition type of value

    >>> print(DefQuery.query('EMACS_MODE_IGNORE_APPS'))
    replacementdef

    >>> print(DefQuery.query('VIRTUALMACHINE'))
    appdef

    >>> print(DefQuery.query('KeyCode::VK_OPEN_URL_WEB_google'))
    vkopenurldef

    >>> print(DefQuery.query_filter('EMACS_MODE_IGNORE_APPS'))
    Filter
    '''

    DATA_DIR = 'data/def'
    DATA_SUFFIX = 'xml'

    QUERY_ORDER = ['appdef',
                   'replacementdef',
                   'devicevendordef',
                   'deviceproductdef',
                   'uielementroledef',
                   'windownamedef',
                   'vkopenurldef',
                   'inputsourcedef',
                   'vkchangeinputsourcedef',]

    def get_data(self, type):
        xml_tree = XML_base.parse(self.get_datapath(type))
        name_val = get_name_tag_by_def_tag(type)

        if name_val == '':
            tags = xml_tree.findall(type)
        else:
            tags = xml_tree.findall('%s/%s' % (type, name_val))

        return list(map(lambda tag: tag.text, tags))

    @classmethod
    def add_def(cls, definition):
        self = cls.get_instance()
        type = definition.get_def_tag_name()
        defname = definition.get_name()
        self.data[type].add(defname)

    @classmethod
    def query_filter(cls, value):
        result = cls.query(value)

        if result is None:
            raise UndefinedFilterException('Undefined filter `%s`' % value)
        else:
            return get_filter_by_def(result.lower())


if __name__ == '__main__':
    import doctest
    doctest.testmod()