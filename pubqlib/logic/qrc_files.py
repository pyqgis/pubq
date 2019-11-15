# -*- coding: utf-8 -*-
"""
Contains the definition of the PubQrc class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

logger = logging.getLogger('PubQrc')


class PubQrc(object):
    """
    This class represents a resource about to be converted.

    Attributes:
        path_in (src):
            The path of the source file.
        path_out (src):
            The path of the source file.
    """

    def __init__(self, path_in, path_out=None):
        """
        Constructor.

        Arguments:
            path_in (src):
                The path of the source file.
            path_out (src):
                The path of the source file.

        """
        super().__init__()
        self.path_in = path_in
        self.path_out = path_out

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'PubQrc()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'PubQrc()'
