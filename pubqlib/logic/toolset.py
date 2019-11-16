# -*- coding: utf-8 -*-
"""
Contains the definition of the Toolset class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import os
import subprocess

logger = logging.getLogger('Toolset')


class Toolset(object):
    """
    This class groups tools used by the program.

    Attributes:

    """

    def __init__(self):
        """
        Constructor.

        Arguments:

        """
        super().__init__()
        self.lupdate = None
        self.lrelease = None
        self.rc_compiler = None
        self.ui_compiler = None
        self.zip_tool = None
        self.find()

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'Toolset()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'Toolset()'

    def find(self):
        """ Locates the tools. """
        self.lupdate = find_app(('pylupdate5', 'pylupdate4'))
        self.lrelease = find_app(('lrelease', 'lrelease-qt5', 'lrelease-qt4'))
        self.rc_compiler = find_app(('pyrcc5', 'pyrcc4'))
        self.ui_compiler = find_app(('pyuic5', 'pyuic4'))
        self.zip_tool = find_app(('zip', '7z'))
        logger.debug("rc_compiler: %r", self.rc_compiler)
        logger.debug("ui_compiler: %r", self.ui_compiler)
        logger.debug("lupdate: %r", self.lupdate)
        logger.debug("lrelease: %r", self.lrelease)
        logger.debug("zip_tool: %r", self.zip_tool)

    def from_args(self, args):
        """ Initialize the paths from arguments. """
        if args.rc_compiler is not None and len(args.rc_compiler) > 0:
            self.rc_compiler = args.rc_compiler
        if args.ui_compiler is not None and len(args.ui_compiler) > 0:
            self.ui_compiler = args.ui_compiler

        logger.debug("rc_compiler: %r", self.rc_compiler)
        logger.debug("ui_compiler: %r", self.ui_compiler)
        logger.debug("lupdate: %r", self.lupdate)
        logger.debug("lrelease: %r", self.lrelease)
        logger.debug("zip_tool: %r", self.zip_tool)

    def prepare_parser(self, parser):
        parser.add_argument(
            "--rc-compiler", default=self.rc_compiler,
            action="store",
            help="the path of the rc compiler")
        parser.add_argument(
            "--ui-compiler", default=self.ui_compiler,
            action="store",
            help="the path of the ui compiler")

    def run(self, command, *arguments):
        """ Executes an outside command. """
        logger.debug("executing %s %r", command, arguments)
        subprocess.check_call([command, *arguments])

    def compile_ui_file(self, in_file, out_file):
        self.run(self.ui_compiler, '-o', out_file, in_file)

    def compile_rc_file(self, in_file, out_file):
        self.run(self.rc_compiler, '-o', out_file, in_file)


def find_app(names):
    """
    Locates an executable within the PATH.

    Adapted from StackExchange:
    http://stackoverflow.com/questions/377017
    """
    if not isinstance(names, (list, tuple, set)):
        names = [names]

    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    def ext_candidates(fpath):
        yield fpath
        for ext in os.environ.get("PATHEXT", "").split(os.pathsep):
            yield fpath + ext

    for app in names:
        path, name = os.path.split(app)
        if path:
            if is_exe(app):
                return app
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                logger.log(1, "searching %s in %s", app, path)
                exe_file = os.path.join(path, app)
                for candidate in ext_candidates(exe_file):
                    if is_exe(candidate):
                        logger.debug("found %s for name %r", candidate, names)
                        return candidate

    logger.debug("could not find an executable for command %r", names)
    return None
