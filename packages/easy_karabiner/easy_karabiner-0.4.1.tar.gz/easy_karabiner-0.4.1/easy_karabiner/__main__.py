# -*- coding: utf-8 -*-
"""A tool to generate key remap configuration for Karabiner

Usage:
    easy_karabiner [-evr] [SOURCE] [TARGET | --string]
    easy_karabiner [--help | --version]
"""
from __future__ import print_function
import os
import click
import lxml
from hashlib import sha1
from subprocess import call
from easy_karabiner import lookup
from easy_karabiner import __version__
from easy_karabiner import exception
from easy_karabiner.xml_base import XML_base
from easy_karabiner.generator import Generator


DEFAULT_CONFIG_PATH = '~/.easy_karabiner.py'
DEFAULT_OUTPUT_PATH = '~/Library/Application Support/Karabiner/private.xml'

DEFAULT_CONFIG_PATH = os.path.expanduser(DEFAULT_CONFIG_PATH)
DEFAULT_OUTPUT_PATH = os.path.expanduser(DEFAULT_OUTPUT_PATH)

VERBOSE = None

@click.command()
@click.help_option('--help', '-h')
@click.version_option(__version__, '--version', '-v', message='%(version)s')
@click.argument('inpath', default=DEFAULT_CONFIG_PATH, type=click.Path())
@click.argument('outpath', default=DEFAULT_OUTPUT_PATH, type=click.Path())
@click.option('--verbose', '-V', help='Print more text.', is_flag=True)
@click.option('--string', '-s', help='Output as string.', is_flag=True)
@click.option('--reload', '-r', help='Reload Karabiner.', is_flag=True)
@click.option('--no-reload', help='Opposite of --reload', is_flag=True)
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

        if xml_str is None:
            exit(1)
        elif options.get('string'):
            print(xml_str)
            exit(0)

        try:
            if not is_generated_by_easy_karabiner(outpath):
                backup_file(outpath)
        except IOError:
            pass

        write_generated_xml(outpath, xml_str)

        # auto reload Karabiner if user not clearly required not reloading
        need_reload = options.get('reload') or (outpath == DEFAULT_OUTPUT_PATH)
        # if `--no_reload` provided, then don't reload Karabiner anyway
        if not options.get('no_reload') and need_reload:
            reload_karabiner()

        exit(0)
    except IOError:
        print("%s not exist" % inpath)
        exit(1)


def read_config_file(config_path):
    configs = {}
    with open(config_path, 'rb') as fp:
        if VERBOSE:
            print('Execute "%s"' % config_path)
        exec(compile(fp.read(), config_path, 'exec'), {}, configs)
    return configs

def write_generated_xml(outpath, content):
    with open(outpath, 'w') as fp:
        if VERBOSE:
            print('Write XML to "%s"' % outpath)
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

    try:
        return Generator(remaps=remaps, definitions=definitions).to_str()
    except exception.ConfigError as e:
        print(e)
        return None

def is_generated_by_easy_karabiner(filepath):
    try:
        tag = XML_base.parse(filepath).find('Easy-Karabiner')
        return tag is not None
    except lxml.etree.XMLSyntaxError:
        return False

def backup_file(filepath, newpath=None):
    with open(filepath, 'rb') as fp:
        if newpath is None:
            # private.xml -> private.941f123.xml
            checksum = sha1(fp.read()).hexdigest()[:7]
            parts = os.path.basename(filepath).split('.')
            parts.insert(-1, checksum)
            newname = '.'.join(parts)

            if VERBOSE:
                print("Backup original XML config file")
            newpath = os.path.join(os.path.dirname(filepath), newname)

        os.rename(filepath, newpath)
        return newpath