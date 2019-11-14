# -*- coding: utf-8 -*-
"""
Contains the definition of the PubModule class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import os
import pkgutil

logger = logging.getLogger('pubq.module')


class PubModule(object):
    """
    This class .

    Attributes:
        name (str):
            the name of the module
        path (str):
            the file system path of the module
        exclude_modules (list):
            a list of module names that we export
    """

    def __init__(self, name, path, exclude_modules=None):
        """
        Constructor.

        Arguments:
            name (str):
                the name of the module
            path (str):
                the file system path of the module
            exclude_modules (list):
                a list of module names that we export
        """
        super().__init__()
        self.name = name
        self.path = path
        self.exclude_modules = [] if exclude_modules is None else exclude_modules
        self.files = []

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'PubModule(#%s)' % self.name

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'PubModule(%r, %r)' % (self.name, self.path)

    def collect_py_files(self,
                         source_py=False, pkg_name=None, pkg_path=None):
        """
        Collects the files in a module.

        Arguments:
            source_py:
                True if the source files are to be collected, False if
                compiled source.
            pkg_name:
                Name of the package
            pkg_path:
                Path in dotted notation.
        """
        if pkg_path is None:
            pkg_path = self.path
        if pkg_name is None:
            pkg_name = self.name

        for importer, modname, is_pkg in pkgutil.walk_packages(
                path=[pkg_path],
                prefix='',
                onerror=lambda x: None):

            if not any(regex.match(modname) for regex in self.exclude_modules):
                fs_name = os.path.join(pkg_path, modname)
                fs_path = module_to_file(fs_name, source_py)
                if fs_path is not None:
                    self.files.append(fs_path)
                    if os.path.isdir(fs_name):
                        self.collect_py_files(
                            source_py=source_py,
                            pkg_name='%s.%s' % (pkg_name, modname),
                            pkg_path=fs_name)


def module_to_file(path, source_py):
    """ Get the file for a module name. """

    if os.path.isdir(path):
        if not source_py:
            tmp = os.path.join(path, "__init__.pyc")
            if os.path.isfile(tmp):
                return tmp
        tmp = os.path.join(path, "__init__.py")
        if os.path.isfile(tmp):
            return tmp
    else:
        if not source_py:
            tmp = path + ".pyc"
            if os.path.isfile(tmp):
                return tmp
        tmp = path + ".py"
        if os.path.isfile(tmp):
            return tmp

    return None
