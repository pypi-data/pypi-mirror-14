# -*- coding: utf-8 -*-
import os
import inspect
import subprocess
from easy_karabiner import exception
from easy_karabiner.xml_base import XML_base


class Hashable(object):
    @property
    def id(self):
        raise exception.NeedOverrideError()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id


def find_all_subclass_of(superclass, global_vars):
    # remove start with '_'
    names = filter(lambda name: not name.startswith('_'), global_vars.keys())
    # remove name which is not a class name
    names = filter(lambda name: inspect.isclass(global_vars[name]), names)
    # remove class name which is not a subclass of superclass
    names = filter(lambda name: issubclass(global_vars[name], superclass), names)
    return list(map(global_vars.get, names))

def remove_all_space(s):
    return ''.join(s.split())

def is_xml_element_equal(node1, node2):
    if len(node1) != len(node2):
        return False
    if node1.tag != node2.tag:
        return False
    if node1.attrib != node2.attrib:
        return False

    text1 = '' if node1.text is None else remove_all_space(node1.text)
    text2 = '' if node2.text is None else remove_all_space(node2.text)
    return text1 == text2

def is_xml_tree_equal(tree1, tree2, ignore_tags=tuple()):
    if tree1.tag == tree2.tag and tree1.tag in ignore_tags:
        return True
    elif is_xml_element_equal(tree1, tree2):
        elems1 = list(tree1)
        elems2 = list(tree2)

        for i in range(len(elems1)):
            if not is_xml_tree_equal(elems1[i], elems2[i], ignore_tags=ignore_tags):
                return False
        return True
    else:
        return False

def assert_xml_equal(xml_tree1, xml_tree2, ignore_tags=tuple()):
    if isinstance(xml_tree1, XML_base):
        xml_tree1 = xml_tree1.to_xml()
    else:
        xml_tree1 = XML_base.parse_string(xml_tree1)

    if isinstance(xml_tree2, XML_base):
        xml_tree2 = xml_tree2.to_xml()
    else:
        xml_tree2 = XML_base.parse_string(xml_tree2)

    assert(is_xml_tree_equal(xml_tree1, xml_tree2, ignore_tags=ignore_tags))

def has_execuable(cmdname):
    with open(os.devnull, "w") as f:
        return subprocess.call(['which', cmdname], stdout=f, stderr=f) == 0

def get_app_path(app_name, default=None):
    if not hasattr(get_app_path, 'apps'):
        if has_execuable('mdfind'):
            cmd = ['mdfind', 'kMDItemContentType==com.apple.application-bundle']
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            output = proc.stdout.read().decode('utf-8')

            app_paths = list(filter(lambda s: len(s.strip()) > 0, output.split('\n')))
            app_names = list(map(os.path.basename, app_paths))

            get_app_path.apps = dict(zip(app_names, app_paths))
        # just for test on Linux
        else:
            get_app_path.apps = dict()

    return get_app_path.apps.get(app_name, default)


def replace_startswith_to(s, startswith, newstart):
    if s.startswith(startswith):
        newval = '%s%s' % (newstart, s.split(startswith, 1)[-1])
        return newval
    else:
        return s