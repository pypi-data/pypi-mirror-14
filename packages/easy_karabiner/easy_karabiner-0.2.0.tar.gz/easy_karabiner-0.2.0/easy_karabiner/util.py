# -*- coding: utf-8 -*-
import os
import inspect
import subprocess
from easy_karabiner.xml_base import XML_base


class Hashable(object):
    def _id(self):
        raise Exception('Need override')

    def __hash__(self):
        return hash(self._id())

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._id() == other._id()


def find_all_subclass_of(superclass, global_vars):
    # remove start with '_'
    names = filter(lambda name: not name.startswith('_'), global_vars.keys())
    # remove name which is not a class name
    names = filter(lambda name: inspect.isclass(global_vars[name]), names)
    # remove class name which is not a subclass of superclass
    names = filter(lambda name: issubclass(global_vars[name], superclass), names)
    return map(global_vars.get, names)


def assert_xml_equal(xml_tree1, xml_tree2):
    if isinstance(xml_tree1, (XML_base, str)):
        xmlstr1 = str(xml_tree1)
    if isinstance(xml_tree2, (XML_base, str)):
        xmlstr2 = str(xml_tree2)

    xmlstr1 = ''.join(xmlstr1.split())
    xmlstr2 = ''.join(xmlstr2.split())

    assert(xmlstr1 == xmlstr2)


def get_apppath(appname, default=None):
    if not hasattr(get_apppath, '_apps'):
        cmd = ['mdfind', 'kMDItemContentType==com.apple.application-bundle']
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        apppaths = filter(lambda path: len(path.strip()) > 0,
                          proc.stdout.read().split('\n'))
        appnames = map(os.path.basename, apppaths)
        get_apppath._apps = dict(zip(appnames, apppaths))

    return get_apppath._apps.get(appname, default)


def replace_startswith_to(s, startswith, newstart):
    if s.startswith(startswith):
        newval = '%s%s' % (newstart, s.split(startswith, 1)[-1])
        return newval
    else:
        return s