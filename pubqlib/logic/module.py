# -*- coding: utf-8 -*-
"""
Contains the definition of the PubModule class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import compileall
import logging
import os
import pkgutil

from .py_files import PubPy


logger = logging.getLogger('pubq.module')


class PubModule(object):
    """
    A module inside the package.

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
        logger.debug("module %s is collecting files from %s(%r)",
                     self.name, pkg_name, pkg_path)
        for importer, modname, is_pkg in pkgutil.walk_packages(
                path=[pkg_path],
                prefix='',
                onerror=lambda x: None):

            if not any(regex.match(modname) for regex in self.exclude_modules):
                fs_name = os.path.join(pkg_path, modname)
                self.files.append(PubPy.module_to_file(fs_name, source_py))
                if os.path.isdir(fs_name):
                    self.collect_py_files(
                        source_py=source_py,
                        pkg_name='%s.%s' % (pkg_name, modname),
                        pkg_path=fs_name)
            else:
                logger.debug("module %r excluded by exclude_modules",
                             modname)

    def compile(self, toolset, force=False):
        """ Create path_out file from path_in. """
        logger.debug("compiling module %s at %s", self.name, self.path)
        compileall.compile_dir(dir=self.path, legacy=True)
        logger.debug("done compiling module %s at %s", self.name, self.path)
