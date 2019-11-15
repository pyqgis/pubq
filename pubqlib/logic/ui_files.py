# -*- coding: utf-8 -*-
"""
Contains the definition of the PubUi class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging

logger = logging.getLogger('PubUi')


class PubUi(object):
    """
    This class .

    Attributes:

    """

    def __init__(self, path_in, path_out=None):
        """
        Constructor.

        Arguments:

        """
        super().__init__()
        self.path_in = path_in
        self.path_out = path_out

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'PubUi()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'PubUi()'
