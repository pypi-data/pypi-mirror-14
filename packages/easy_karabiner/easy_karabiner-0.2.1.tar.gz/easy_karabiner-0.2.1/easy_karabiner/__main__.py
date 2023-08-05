# -*- coding: utf-8 -*-
"""A tool to generate key remap configuration for Karabiner

Usage:
    easy_karabiner [-r] [-h | -v | -e | -s | -o PATH] [FILE]

Examples:
    easy_karabiner
    easy_karabiner -s "~/.easy_karabiner.py"
    easy_karabiner -o "~/Library/Application Support/Karabiner/private.xml"

Options:
    -h --help
    -v --version             Show version
    -s --string              output as string
    -o PATH --output=PATH    specify output file path
    -r --reload              reload Karabiner
    -e --edit                edit "~/.easy_karabiner.py"
"""
from __future__ import print_function

import os
from hashlib import sha1
from subprocess import call
from docopt import docopt
from easy_karabiner import lookup
from easy_karabiner import __version__
from easy_karabiner.xml_base import XML_base
from easy_karabiner.generator import Generator


def gen_config(remaps, definitions=None):
    return Generator(remaps=remaps, definitions=(definitions or [])).generate()

def is_original_config(filepath):
    try:
        tag = XML_base.parse(filepath).find('Easy-Karabiner')
        return tag is None
    except:
        return True

def backup_file(filepath):
    checksum = sha1(open(filepath, 'rb').read()).hexdigest()[:7]
    parts = os.path.basename(filepath).split('.')
    parts.insert(-1, checksum)
    newname = os.path.join(os.path.dirname(filepath), '.'.join(parts))
    os.rename(filepath, newname)

def reload_karabiner():
    call(['karabiner', 'enable', 'private.easy_karabiner'])
    call(['karabiner', 'reloadxml'])
    print("Reload Karabiner config xml file.")

def main():
    DEFAULT_CONFIG = os.path.expanduser("~/.easy_karabiner.py")
    DEFAULT_OUTPUT = os.path.expanduser("~/Library/Application Support/Karabiner/private.xml")

    args = docopt(__doc__)
    config_path = os.path.expanduser(args['FILE'] or DEFAULT_CONFIG)
    output_path = os.path.expanduser(args['--output'] or DEFAULT_OUTPUT)
    output_as_str = args['--string']
    need_reload = args['--reload']
    need_edit = args['--edit']
    show_version = args['--version']

    if show_version:
        print(__version__)
        return
    elif need_edit:
        editor = os.environ.get('EDITOR', 'vi')
        call([editor, os.path.expanduser(DEFAULT_CONFIG)])
        return

    variables = {}
    if os.path.isfile(config_path):
        with open(config_path) as fp:
            exec(compile(fp.read(), config_path, 'exec'), {}, variables)
    else:
        print("Can't find config file \"%s\"" % config_path)
        return

    remaps = variables.get('REMAPS', [])
    definitions = variables.get('DEFINITIONS', [])

    # user may define it's own alias table
    lookup.update_key_alias(variables.get('KEY_ALIAS', {}))
    lookup.update_def_alias(variables.get('DEF_ALIAS', {}))
    lookup.update_keymap_alias(variables.get('KEYMAP_ALIAS', {}))

    xml_str = gen_config(remaps=remaps, definitions=definitions)

    if output_as_str:
        print(xml_str)
    else:
        if is_original_config(output_path):
            backup_file(output_path)
        with open(output_path, 'wb') as fp:
            fp.write(xml_str)

        if need_reload or (output_path == DEFAULT_OUTPUT):
            reload_karabiner()


if __name__ == "__main__":
    main()
