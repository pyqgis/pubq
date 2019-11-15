# -*- coding: utf-8 -*-
"""
Contains the definition of the PubUi class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import os

from .file_base import PubFile

logger = logging.getLogger('PubUi')


class PubUi(PubFile):
    """
    This class .

    Attributes:

    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Arguments:

        """
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'PubUi("%s")' % self.path_in

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'PubUi(path_in=%r, path_out=%r, use_compiled=%r)' % (
            self.path_in,
            self.path_out,
            self.use_compiled,
        )

    def default_output(self):
        """ Computes the default output file. """
        base_path, file_name = os.path.split(self.path_in)
        file_name, file_ext = os.path.splitext(file_name)
        result = os.path.join(base_path, "ui_{0}.py".format(file_name))
        logger.debug("computed default output file for %r to be %r",
                     self.path_in, result)
        return result

    def compile(self, toolset, force=False):
        """ Create path_out file from path_in. """
        if not self.use_compiled:
            logger.debug("%r will not be compiled because "
                         "use_compiled is false", self.path_in)
            return

        if self.path_out is None:
            self.path_out = self.default_output()

        logger.debug("compiling %r to %r", self.path_in, self.path_out)
        toolset.compile_ui_file(
            in_file=self.path_in, out_file=self.path_out)
