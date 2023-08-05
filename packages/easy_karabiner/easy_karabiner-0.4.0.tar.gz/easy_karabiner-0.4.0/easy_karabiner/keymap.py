# -*- coding: utf-8 -*-
from __future__ import print_function
from easy_karabiner import util
from easy_karabiner import alias
from easy_karabiner import exception
from easy_karabiner.xml_base import XML_base
from easy_karabiner.key import Key


class BaseKeyToKey(XML_base, util.Hashable):
    MULTI_KEYS_FMT = '@begin\n{key}\n@end'
    AUTOGEN_FMT = ' {type}\n{keys_str}\n'

    def __init__(self, *keys, **kwargs):
        self.keys_str = self.parse(*keys, **kwargs)

    def parse(self, *keys, **kwargs):
        raise exception.NeedOverrideError()

    def get_type(self):
        return '__%s__' % self.get_clsname()

    def to_xml(self):
        text = self.AUTOGEN_FMT.format(type=self.get_type(),
                                       keys_str=self.keys_str)
        return self.create_tag('autogen', text)

    @property
    def id(self):
        return (self.get_type(), self.keys_str)

class UniversalKeyToKey(BaseKeyToKey):
    def __init__(self, type, *keys, **kwargs):
        self.type = type
        super(UniversalKeyToKey, self).__init__(*keys, **kwargs)

    def get_type(self):
        return self.type

    def parse(self, *keys, **kwargs):
        toKey = lambda k: Key(k, keep_first_keycode=True, has_modifier_none=False)
        keys = map(toKey, keys)
        keys = map(str, keys)

        return ',\n'.join(keys)


class _KeyToMultiKeys(BaseKeyToKey):
    KEYS_FMT = ('{from_key},\n'
                '@begin\n'
                '{to_key}\n'
                '@end\n'
                '@begin\n'
                '{additional_key}\n'
                '@end')

    def parse(self, from_key, additional_key, to_key=None, has_modifier_none=True):
        if to_key:
            to_key = Key(to_key)
        else:
            to_key = Key(from_key)

        from_key = Key(from_key, has_modifier_none)
        additional_key = Key(additional_key)

        return self.KEYS_FMT.format(from_key=from_key.to_str(),
                                    to_key=to_key.to_str(),
                                    additional_key=additional_key.to_str())

class _OneKeyEvent(BaseKeyToKey):
    def parse(self, key, has_modifier_none=False):
        return Key(key, has_modifier_none).to_str()

class _ZeroKeyEvent(BaseKeyToKey):
    def parse(self):
        return ''

class _MultiKeys(UniversalKeyToKey):
    def __init__(self, *keys, **kwargs):
        super(_MultiKeys, self).__init__(self.get_type(), *keys, **kwargs)

    def get_type(self):
        return '__%s__' % self.get_clsname()


class KeyToKey(BaseKeyToKey):
    '''
    >>> print(KeyToKey('alt', 'cmd'))
    <autogen>__KeyToKey__ KeyCode::OPTION_L, KeyCode::COMMAND_L</autogen>
    '''

    KEYS_FMT = '{from_key},\n{to_key}'

    def parse(self, from_key, to_key, has_modifier_none=True):
        from_key = Key(from_key, has_modifier_none=has_modifier_none)
        to_key = Key(to_key)

        return self.KEYS_FMT.format(from_key=from_key.to_str(),
                                    to_key=to_key.to_str())

class DropAllKeys(BaseKeyToKey):
    KEYS_FMT = '{from_key},\n{options}'

    def parse(self, from_modifier, options=None):
        from_key = Key(from_modifier, keep_first_keycode=True)

        if options is None:
            return from_key.to_str()
        else:
            options = Key(options, keep_first_keycode=True)
            return self.KEYS_FMT.format(from_key=from_key.to_str(),
                                        options=options.to_str())

class SimultaneousKeyPresses(BaseKeyToKey):
    KEYS_FMT = ('@begin\n'
                '{from_key}\n'
                '@end\n'
                '@begin\n'
                '{to_key}\n'
                '@end')

    def parse(self, from_key, to_key):
        from_key = Key(from_key, False)
        to_key = Key(to_key, False)

        return self.KEYS_FMT.format(from_key=from_key.to_str(),
                                    to_key=to_key.to_str())


class DoublePressModifier(_KeyToMultiKeys):
    pass

class HoldingKeyToKey(_KeyToMultiKeys):
    pass

class KeyOverlaidModifier(_KeyToMultiKeys):
    pass

class KeyDownUpToKey(_KeyToMultiKeys):
    def parse(self, from_key, immediately_key, interrupted_key):
        return super(KeyDownUpToKey, self).parse(from_key,
                                                 interrupted_key,
                                                 immediately_key)


class BlockUntilKeyUp(_OneKeyEvent):
    pass

class DropKeyAfterRemap(_OneKeyEvent):
    pass


class PassThrough(_ZeroKeyEvent):
    pass

class DropPointingRelativeCursorMove(_ZeroKeyEvent):
    pass


# NOTICE: because below `autogen` command not yet documented,
#         so those implements maybe changed in future
class DropScrollWheel(_MultiKeys):
    pass

class FlipPointingRelative(_MultiKeys):
    pass

class FlipScrollWheel(_MultiKeys):
    pass

class IgnoreMultipleSameKeyPress(_MultiKeys):
    pass

class StripModifierFromScrollWheel(_MultiKeys):
    pass

class ScrollWheelToScrollWheel(_MultiKeys):
    pass

class ScrollWheelToKey(_MultiKeys):
    pass

class PointingRelativeToScroll(_MultiKeys):
    pass

class PointingRelativeToKey(_MultiKeys):
    pass

class ForceNumLockOn(_MultiKeys):
    pass

class ShowStatusMessage(BaseKeyToKey):
    def parse(self, *keys, **kwargs):
        return ' '.join(keys)

class SetKeyboardType(_OneKeyEvent):
    pass


_CLASSES = util.find_all_subclass_of(BaseKeyToKey, globals())

def get_ground_truth_vals(clsname, vals):
    def replace_vkopenurl_start(val):
        return util.replace_startswith_to(val, 'Open::', 'KeyCode::VK_OPEN_URL_')

    vals = list(map(replace_vkopenurl_start, vals))
    return vals

def create_keymap(clsname, command, keys):
    for cls in _CLASSES:
        if clsname == cls.__name__:
            return cls(*keys)

    return UniversalKeyToKey(command, *keys)

def parse_keymap(command, keys):
    '''
    Parse `[(command), key1, key2, ...]` and return relative keymap
    '''
    clsname = alias.get_alias('KEYMAP_ALIAS', command, command.strip('_'))
    keys = get_ground_truth_vals(clsname, keys)
    keymap = create_keymap(clsname, command, keys)
    return keymap


if __name__ == "__main__":
    import doctest
    doctest.testmod()