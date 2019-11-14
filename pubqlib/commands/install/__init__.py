# -*- coding: utf-8 -*-
"""

"""
import logging

logger = logging.getLogger('pubq.command.install')


def install_command(args, log):
    """ The command handler for version command. """
    pass


def create_install_command(subparsers):
    """ Construct the parser for program arguments. """
    parser = subparsers.add_parser(
        'install', help='Installs a plugin to local QGis installation')
    parser.set_defaults(func=install_command)
