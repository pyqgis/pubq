# -*- coding: utf-8 -*-
"""
Contains the definition of the PubFile class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import os

logger = logging.getLogger('PubFile')


class PubFile(object):
    """
    Base class for all source files that might be converted..

    Attributes:
        path_in (src):
            The path of the source file.
        path_out (src):
            The path of the compiled file.
    """

    def __init__(self, path_in=None, path_out=None, use_compiled=True):
        """
        Constructor.

        Arguments:
            path_in (src):
                The path of the source file.
            path_out (src):
                The path of the compiled file.
        """
        super().__init__()
        self.path_in = path_in
        self.path_out = path_out
        self.use_compiled = use_compiled

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'PubFile("%s")' % self.path_in

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'PubFile(path_in=%r, path_out=%r, use_compiled=%r)' % (
            self.path_in,
            self.path_out,
            self.use_compiled,
        )

    @property
    def copy_target(self):
        """ The file that should be copied by the deploy process. """
        return self.path_out if self.use_compiled else self.path_in

    def default_output(self):
        """ Computes the default output file. """
        raise NotImplementedError

    def compile(self, toolset, force=False):
        """ Create path_out file from path_in. """
        raise NotImplementedError

    def changed(self):
        """ Tell if the output is older than input. """
        try:
            infile_s = os.stat(self.path_in)
            outfile_s = os.stat(self.path_out)
            return infile_s.st_mtime > outfile_s.st_mtime
        except IOError:
            return True
