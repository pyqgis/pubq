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
        self.lupdate = find_app(('pylupdate5', 'pylupdate4'))
        self.lrelease = find_app(('lrelease', 'lrelease-qt5', 'lrelease-qt4'))
        self.rc_compiler = find_app(('pyrcc5', 'pyrcc4'))
        self.ui_compiler = find_app(('pyuic5', 'pyuic4'))
        self.zip_tool = find_app(('zip', '7z'))

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'Toolset()'

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'Toolset()'

    def from_args(self, args):
        """ Initialize the paths from arguments. """
        self.rc_compiler = args.rc_compiler
        self.ui_compiler = args.ui_compiler

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
                exe_file = os.path.join(path, app)
                for candidate in ext_candidates(exe_file):
                    if is_exe(candidate):
                        return candidate

    return None
