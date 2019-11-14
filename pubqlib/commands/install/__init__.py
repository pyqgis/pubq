# -*- coding: utf-8 -*-
"""

"""
import logging
import os
import pkgutil
import configparser

from pubqlib.logic.plugin import PubPlugin

logger = logging.getLogger('pubq.command.install')


def install_command(args, log):
    """ The command handler for version command. """
    source = os.path.abspath(args.source)
    source_py = bool(args.source_py)
    plugin = PubPlugin()
    plugin.init_from_directory(source, source_py=source_py)


def create_install_command(subparsers):
    """ Construct the parser for program arguments. """
    parser = subparsers.add_parser(
        'install', help='Installs a plugin to local QGis installation')
    parser.add_argument(
        "--source-py", default=False,
        action="store_true",
        help="deploy source files; by default the program deploys compiled "
             ".pyc files")
    parser.add_argument(
        "source", nargs='+',
        help="The source directory from where we install the plugin")

    parser.set_defaults(func=install_command)
