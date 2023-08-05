# -*- coding: utf-8 -*-
'''Define aliases here. Alias is a dict with lowercase key.

NOTICE: `MODIFIER_ALIAS` is used in both `modifier_only/modifier_not` filter
        and `keymap`, so update `KEY_ALIAS` whenever `MODIFIER_ALIAS` updated.
'''

DEF_ALIAS = {
   'window':  'WindowName',
   'open': 'VKOpenURL',
   'inputsource': 'ChangeInputSource',
}

KEYMAP_ALIAS = {
   'double':  'DoublePressModifier',
   'holding': 'HoldingKeyToKey',
   'press_modifier': 'KeyOverlaidModifier',
}

MODIFIER_ALIAS = {
    "shift"   : "SHIFT_L",
    "shift_l" : "SHIFT_L",
    "shift_r" : "SHIFT_R",
    "cmd"     : "COMMAND_L",
    "command" : "COMMAND_L",
    "cmd_l"   : "COMMAND_L",
    "cmd_r"   : "COMMAND_R",
    "opt"     : "OPTION_L",
    "option"  : "OPTION_L",
    "opt_l"   : "OPTION_L",
    "opt_r"   : "OPTION_R",
    "alt"     : "OPTION_L",
    "alt_l"   : "OPTION_L",
    "alt_r"   : "OPTION_R",
    "ctrl"    : "CONTROL_L",
    "control" : "CONTROL_L",
    "ctrl_l"  : "CONTROL_L",
    "ctrl_r"  : "CONTROL_R",
    "caps"    : "CAPSLOCK",
    "fn"      : "FN",
}

KEY_ALIAS = {
    "whitespace" : "SPACE",
    "sp"         : "SPACE",
    "del"        : "DELETE",
    "fdel"       : "FORWARD_DELETE",
    "esc"        : "ESCAPE",
    "left"       : "CURSOR_LEFT",
    "right"      : "CURSOR_RIGHT",
    "down"       : "CURSOR_DOWN",
    "up"         : "CURSOR_UP",
    "`"          : "BACKQUOTE",
    "1"          : "KEY_1",
    "2"          : "KEY_2",
    "3"          : "KEY_3",
    "4"          : "KEY_4",
    "5"          : "KEY_5",
    "6"          : "KEY_6",
    "7"          : "KEY_7",
    "8"          : "KEY_8",
    "9"          : "KEY_9",
    "0"          : "KEY_0",
    "-"          : "MINUS",
    "="          : "EQUAL",
    "["          : "BRACKET_LEFT",
    "]"          : "BRACKET_RIGHT",
    "\\"         : "BACKSLASH",
    ";"          : "SEMICOLON",
    "'"          : "QUOTE",
    ","          : "COMMA",
    "."          : "DOT",
    "/"          : "SLASH",

    "mouse_left"   : "PointingButton::LEFT",
    "mouse_right"  : "PointingButton::RIGHT",
    "mouse_middle" : "PointingButton::MIDDLE",
    "mouse1"       : "PointingButton::LEFT",
    "mouse2"       : "PointingButton::RIGHT",
    "mouse3"       : "PointingButton::MIDDLE",

    "scroll_up"    : "ScrollWheel::UP",
    "scroll_down"  : "ScrollWheel::DOWN",
    "scroll_left"  : "ScrollWheel::left",
    "scroll_right" : "ScrollWheel::right",
}


KEY_ALIAS.update(MODIFIER_ALIAS)
_ALIASES = dict((k, globals()[k]) for k in globals().keys() if k.endswith('_ALIAS'))

# alias is case-insensitive
def get_alias(tblname, k, d=None):
    return _ALIASES[tblname].get(k.lower(), d)

def update_alias(tblname, aliases):
    _ALIASES.setdefault(tblname, {}).update(aliases)
    if tblname == 'MODIFIER_ALIAS':
        _ALIASES['KEY_ALIAS'].update(_ALIASES['MODIFIER_ALIAS'])