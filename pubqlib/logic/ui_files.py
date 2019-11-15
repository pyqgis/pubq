# -*- coding: utf-8 -*-
"""
Contains the definition of the PubUi class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

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
        return 'PubUi()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'PubUi()'

    def compile(self, toolset, force=False):
        """ Create path_out file from path_in. """
        if not self.use_compiled:
            return
        toolset.compile_ui_file(
            in_file=self.path_in, out_file=self.path_out)
