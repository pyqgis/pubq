# -*- coding: utf-8 -*-
"""
Contains the definition of the PubPy class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import os

from .file_base import PubFile

logger = logging.getLogger('PubPy')


class PubPy(PubFile):
    """
    This class represents a python source file.

    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.

        Arguments:
            path_in (src):
                The path of the source file.
            path_out (src):
                The path of the compiled file.

        """
        super().__init__(*args, **kwargs)

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'PubPy()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'PubPy()'

    @staticmethod
    def module_to_file(path, source_py):
        """
        Get the file for a module name.

        Arguments:
            path (str):
                The path to check
            source_py (bool):
                True to only check for source files.
                False to check for compiled variant.

        Returns:
            PubPy instance
        """
        result = PubPy()
        if os.path.isdir(path):
            result.path_in = os.path.join(path, "__init__.py")
            result.path_out = os.path.join(path, "__init__.pyc")
        else:
            result.path_in = path + ".py"
            result.path_out = path + ".pyc"
        result.use_compiled = not source_py
        return result

