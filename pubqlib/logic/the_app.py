# -*- coding: utf-8 -*-
"""
Contains the definition of the TheApp class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import os

from pubqlib.logic.plugin import PubPlugin
from pubqlib.logic.toolset import Toolset

logger = logging.getLogger('TheApp')


class TheApp(object):
    """
    This class .

    Attributes:

    """

    def __init__(self):
        """
        Constructor.

        Arguments:

        """
        super().__init__()
        self.toolset = Toolset()
        self.source_py = False
        self.destination = None
        self.plugins = []

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'TheApp()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'TheApp()'

    def install(self, sources, force_recompile=False, clear_opt='error'):
        """ The install command is implemented here. """
        logger.debug("Installing %r (forced=%r, clear_opt=%r",
                     sources, force_recompile, clear_opt)
        if not os.path.isdir(self.destination):
            logger.debug("Destination %s does not exist; creating ...",
                         self.destination)
            os.makedirs(self.destination)

        for source in sources:
            source = os.path.abspath(source)
            plugin = PubPlugin()
            plugin.init_from_directory(source, source_py=self.source_py)
            self.plugins.append(plugin)
        logger.debug("Collected %d plugins", len(self.plugins))

        for plugin in self.plugins:
            plugin.compile(toolset=self.toolset, force=force_recompile)
            plugin.deploy(self.destination, clear_opt=clear_opt)

        logger.debug("Installing done")

    def get_plugin_directory(self):
        home = os.path.expanduser('~')
        self.destination = os.path.join(home, '.qgis2', 'python', 'plugins')
        logger.debug("detected qgis plugin directory is at %s",
                     self.destination)
        return self.destination
