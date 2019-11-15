#!/bin/env python
# -*- coding: utf-8 -*-
"""
Central script that allows the user to issue commands.

Usage:

    pubq.py command options
"""
from appupup.main import main

from pubqlib.commands.install import create_install_command
from pubqlib.constants import (__package_name__, __author__, __package_url__)
from pubqlib.__version__ import __version__


def print_version(args, logger, the_app):
    """ The command handler for version command. """
    print("%s version %s" % (__package_name__, __version__))


def setup_parser(parent_parser):
    """ Create the structure that parses the arguments. """
    subparsers = parent_parser.add_subparsers(help='top level command')

    parser = subparsers.add_parser(
        'version', help='Prints the version and exits')
    parser.set_defaults(func=print_version)

    create_install_command(subparsers, my_app)


if __name__ == '__main__':
    from pubqlib.logic.the_app import TheApp
    my_app = TheApp()

    import sys
    sys.exit(main(
        app_name=__package_name__, app_version=__version__,
        app_stage='',
        app_author=__author__,
        app_description='A tool for QGis python plugins.',
        app_url=__package_url__,
        parser_constructor=setup_parser,
        the_app=my_app))
