# -*- coding: utf-8 -*-
"""

"""
import logging
import os
import pkgutil
import configparser

from pubqlib.logic.plugin import PubPlugin
from pubqlib.logic.toolset import Toolset

logger = logging.getLogger('pubq.cmd.install')


def install_command(args, log, the_app):
    """ The command handler for version command. """
    logger.debug("install command (%r)", args)
    the_app.source_py = bool(args.source_py)
    the_app.destination = os.path.abspath(args.destination)
    the_app.toolset.from_args(args)
    the_app.install(
        args.source,
        force_recompile=args.force_recompile,
        clear_opt=args.on_existing,
    )


def create_install_command(subparsers, the_app):
    """ Construct the parser for program arguments. """
    parser = subparsers.add_parser(
        'install', help='Installs a plugin to local QGis installation')

    # The toolset also gets some arguments here.
    the_app.toolset.prepare_parser(parser)

    destination = the_app.get_plugin_directory()

    parser.add_argument(
        "--source-py", default=False,
        action="store_true",
        help="deploy source files; by default the program deploys compiled "
             ".pyc files")
    parser.add_argument(
        "--force-recompile", default=False,
        action="store_true",
        help="forces the recompilation even if the timestamps would suggest "
             "that there's no need")
    parser.add_argument(
        "--destination", default=destination,
        help="where to copy the files")
    parser.add_argument(
        "--on-existing", default='error',
        choices=['error', 'clear', 'overwrite'],
        help="what to do when the target directory exists; can be "
             "error (will refuse to go forward if the directory is not empty), "
             "clear (will delete any files or  directories found inside prior to installation) or "
             "overwrite (will only overwrite the files that are installed)")
    parser.add_argument(
        "source", nargs='+',
        help="The source directory from where we install the plugin")

    parser.set_defaults(func=install_command)
