# -*- coding: utf-8 -*-
"""A tool to generate key remap configuration for Karabiner

Usage:
    easy_karabiner [-evr] [SOURCE] [TARGET | --string]
    easy_karabiner [--help | --version]
"""
from __future__ import print_function
import os
import click
from hashlib import sha1
from subprocess import call
from easy_karabiner import lookup
from easy_karabiner import __version__
from easy_karabiner.xml_base import XML_base
from easy_karabiner.generator import Generator


DEFAULT_CONFIG_PATH = '~/.easy_karabiner.py'
DEFAULT_OUTPUT_PATH = '~/Library/Application Support/Karabiner/private.xml'

DEFAULT_CONFIG_PATH = os.path.expanduser(DEFAULT_CONFIG_PATH)
DEFAULT_OUTPUT_PATH = os.path.expanduser(DEFAULT_OUTPUT_PATH)


@click.command()
@click.help_option('--help', '-h')
@click.version_option(__version__, '--version', '-v', message='%(version)s')
@click.argument('inpath', default=DEFAULT_CONFIG_PATH, type=click.Path())
@click.argument('outpath', default=DEFAULT_OUTPUT_PATH, type=click.Path())
@click.option('--verbose', '-V', help='Print more text.', is_flag=True)
@click.option('--string', '-s', help='Output as string.', is_flag=True)
@click.option('--reload', '-r', help='Reload Karabiner.', is_flag=True)
@click.option('--edit', '-e', help='Edit default config file.', is_flag=True)
def main(inpath, outpath, **options):
    """
    \b
    $ easy_karabiner
    $ easy_karabiner input.py output.xml
    $ easy_karabiner input.py --string
    """
    global VERBOSE
    VERBOSE = options.get('verbose')

    if options.get('edit'):
        edit_config_file()
        exit(0)

    try:
        configs = read_config_file(inpath)
        xml_str = gen_config(configs)

        if options.get('string'):
            print(xml_str)
            exit(0)

        try:
            if not is_generated_by_easy_karabiner(outpath):
                backup_file(outpath)
        except IOError:
            pass

        write_generated_xml(outpath, xml_str)

        if options.get('reload') or (outpath == DEFAULT_OUTPUT_PATH):
            reload_karabiner()

        exit(0)
    except IOError:
        print("%s not exist" % inpath)
        exit(1)


def read_config_file(config_path):
    configs = {}
    with open(config_path, 'rb') as fp:
        if VERBOSE:
            print("Execute %s" % config_path)
        exec(compile(fp.read(), config_path, 'exec'), {}, configs)
    return configs

def write_generated_xml(outpath, content):
    with open(outpath, 'wb') as fp:
        if VERBOSE:
            print("Write generated XML config to %s" % outpath)
        fp.write(content)

def edit_config_file():
    editor = os.environ.get('EDITOR', 'vi')
    call([editor, DEFAULT_CONFIG_PATH])

def reload_karabiner():
    if VERBOSE:
        print("Reload Karabiner config")
    call(['karabiner', 'enable', 'private.easy_karabiner'])
    call(['karabiner', 'reloadxml'])

def update_aliases(configs):
    if VERBOSE:
        print("Update alias database")
    # user may define it's own alias table
    alias_names = filter(lambda k: k.endswith('_ALIAS'), configs.keys())
    for alias_name in alias_names:
        lookup.update_alias(configs[alias_name])

def gen_config(configs):
    remaps = configs.get('REMAPS', [])
    definitions = configs.get('DEFINITIONS', [])
    update_aliases(configs)
    if VERBOSE:
        print("Generate XML configuration string")
    return Generator(remaps=remaps, definitions=definitions).generate()

def is_generated_by_easy_karabiner(filepath):
    tag = XML_base.parse(filepath).find('Easy-Karabiner')
    return tag is not None

def backup_file(filepath):
    with open(filepath, 'rb') as fp:
        checksum = sha1(fp.read()).hexdigest()[:7]
        parts = os.path.basename(filepath).split('.')
        parts.insert(-1, checksum)
        newname = os.path.join(os.path.dirname(filepath), '.'.join(parts))
        if VERBOSE:
            print("Backup original XML config file")
        # private.xml -> private.941f123.xml
        os.rename(filepath, newname)