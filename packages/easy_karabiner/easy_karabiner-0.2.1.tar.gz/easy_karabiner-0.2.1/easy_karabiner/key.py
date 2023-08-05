# -*- coding: utf-8 -*-
from __future__ import print_function

from easy_karabiner.lookup import get_key_alias, KeyCodeQuery

class Key(object):
    """Convert space seperated string to Karabiner's favorite format

    >>> print(Key('shift_l Cmd'))
    KeyCode::SHIFT_L, ModifierFlag::COMMAND_L
    """

    def __init__(self, keys='', has_modifier_none=False, keep_first_keycode=False):
        self.has_modifier_none = has_modifier_none
        self.keep_first_keycode = keep_first_keycode
        self.keys = self.parse(keys)

    def parse(self, keys):
        # remove multiple whitespaces and convert to raw value
        keys = " ".join(keys.split()).split()
        # if no alias find, then return the original value
        keys = map(get_key_alias, keys)
        # if no key header find, then return the original value
        keys = map(self.add_key_header, keys)
        # we need adjust position of keys, because
        # the first key can't be modifier key in most case
        keys = self.rearrange_keys(list(keys))

        if len(keys) > 0:
            if not self.keep_first_keycode and self.is_modifier_key(keys[0]):
                # change the header of first key to `KeyCode`
                keys = self.regularize_first_key(keys)
            if self.has_modifier_none and self.is_modifier_key(keys[-1]):
                keys = self.add_modifier_none(keys)

        return keys

    def add_key_header(self, key):
        header = KeyCodeQuery.query(key.upper())
        if header is None:
            return key
        else:
            return "%s::%s" % (header, key.upper())

    def rearrange_keys(self, keys):
        tmp = []
        last = 0

        for i in range(len(keys)):
            if not self.is_modifier_key(keys[i]):
                tmp.append(keys[i])
                while last < i:
                    tmp.append(keys[last])
                    last += 1
                last = i + 1

        tmp.extend(keys[last:])
        return tmp

    def is_modifier_key(self, key):
        return key.lower().startswith('modifier')

    def regularize_first_key(self, keys):
        parts = keys[0].split(':')
        keys[0] = 'KeyCode::' + parts[-1]
        return keys

    # if there  need append 'ModifierFlag::NONE' if you want change from this key
    # For more information about 'ModifierFlag::NONE', see https://pqrs.org/osx/karabiner/xml.html.en
    def add_modifier_none(self, keys):
        keys.append('ModifierFlag::NONE')
        return keys

    def to_str(self):
        return ', '.join(self.keys)

    def __add__(self, another):
        res = Key()
        res.keys = self.keys + another.keys
        res.has_modifier_none = self.has_modifier_none or another.has_modifier_none
        res.keep_first_keycode = self.keep_first_keycode or another.keep_first_keycode
        return res

    def __str__(self):
        return self.to_str()


if __name__ == "__main__":
    import doctest
    doctest.testmod()