# -*- coding: utf-8 -*-
"""
Contains the definition of the PubPlugin class.
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
import os

import configparser

from .module import PubModule
from .qrc_files import PubQrc
from .ui_files import PubUi

logger = logging.getLogger('pubq.plugin')


class PubPlugin(object):
    """
    This class .

    Attributes:

        modules (list):
            The list of modules in this package.
    """

    def __init__(self, source_path=None, modules=None,
                 about=None, author=None, category=None, changelog=None,
                 deprecated=None, description=None, email=None, experimental=None,
                 has_processing_provider=None, homepage=None, icon=None,
                 name=None, plugin_dependencies=None, qgis_maximum_version=None,
                 qgis_minimum_version=None, repository=None, tags=None,
                 tracker=None, version=None):
        """
        Constructor.

        Arguments:
            source_path (str):
                The path towards this plugin source.
            modules (list):
                The list of modules in this package.
            name (str):
                a short string containing the name of the plugin
            qgis_minimum_version (str):
                dotted notation of minimum QGIS version
            qgis_maximum_version (str):
                dotted notation of maximum QGIS version
            description (str):
                short text which describes the plugin, no HTML allowed
            about (str):
                longer text which describes the plugin in details,
                no HTML allowed
            version (str):
                short string with the version dotted notation
            author (str):
                author name
            email (str):
                email of the author, only shown on the website to logged
                in users, but visible in the Plugin Manager after the plugin
                is installed
            changelog (str):
                string, can be multiline, no HTML allowed
            experimental (str):
                boolean flag, True or False
            deprecated (str):
                boolean flag, True or False, applies to the whole plugin and
                not just to the uploaded version
            tags (list):
                comma separated list, spaces are allowed inside individual tags
            homepage (str):
                a valid URL pointing to the homepage of your plugin
            repository (str):
                a valid URL for the source code repository
            tracker (str):
                a valid URL for tickets and bug reports
            icon (str):
                a file name or a relative path (relative to the base folder
                of the plugin’s compressed package) of a web friendly
                image (PNG, JPEG)
            category (str):
                one of Raster, Vector, Database and Web
            plugin_dependencies (str):
                PIP-like comma separated list of other plugins to install
            has_processing_provider (str):
                boolean flag, True or False, determines if the plugin
                provides processing algorithms

        """
        super().__init__()
        self.source_path = source_path
        self.config_obj = configparser.ConfigParser(
            comment_prefixes='/', allow_no_value=True)
        self.modules = [] if modules is None else modules
        self.extra_files = []
        self.ui_files = []
        self.qrc_files = []

        # ---- Metadata ----
        self.about = about
        self.author = author
        self.category = category
        self.changelog = changelog
        self.deprecated = deprecated
        self.description = description
        self.email = email
        self.experimental = experimental
        self.has_processing_provider = has_processing_provider
        self.homepage = homepage
        self.icon = icon
        self.name = name
        self.plugin_dependencies = plugin_dependencies
        self.qgis_maximum_version = qgis_maximum_version
        self.qgis_minimum_version = qgis_minimum_version
        self.repository = repository
        self.tags = [] if modules is None else modules
        self.tracker = tracker
        self.version = version

    def __str__(self):
        """ Represent this object as a human-readable string. """
        return 'PubPlugin(#%s)' % (
            self.name if self.name is not None else 'invalid')

    def __repr__(self):
        """ Represent this object as a python constructor. """
        return 'PubPlugin()'

    def init_from_directory(self, path, source_py=False):
        """
        Initializes an empty instance to the content of the directory.

        Arguments:
            path (str):
                The path towards the plugin.
            source_py (bool):
                Set to true to force collection of source files.
        """
        self.source_path = path

        metadata_path = os.path.join(path, 'metadata.txt')
        if not os.path.isfile(metadata_path):
            logger.error('The metadata file is required; should be at %s',
                         metadata_path)
            return False
        self.read_metadata(metadata_path)

        init_path = os.path.join(path, '__init__.py')
        if not os.path.isfile(init_path):
            logger.error('The __init__.py file is required; should be at %s',
                         metadata_path)
            return False
        modules = self.parse_init(init_path)

        self.modules = self.load_modules(path, modules, source_py=source_py)
        self.extra_files = self.load_extra_files(path)
        self.ui_files = self.load_ui_files(path)
        self.qrc_files = self.load_qrc_files(path)

    def has_required_metadata(self):
        """
        Checks that all required metadata is present.

        Returns:
            True if the required fields are present, false otherwise.
        """
        def check_one(attr):
            attr_val = getattr(self, attr)
            if attr_val is None or len(attr_val) == 0:
                logger.error("Missing required field %s", attr)
                return False
            else:
                return True
        return \
            check_one('name') and check_one('qgis_minimum_version') and \
            check_one('description') and check_one('about') and \
            check_one('version') and check_one('author') and \
            check_one('email') and check_one('repository')

    def to_metadata(self):
        """
        Saves the attributes to config object.
        """
        if not self.has_required_metadata():
            return False
        self.config_obj.set(
            'general', 'about', self.about)
        self.config_obj.set(
            'general', 'author', self.author)
        self.config_obj.set(
            'general', 'category', self.category)
        self.config_obj.set(
            'general', 'changelog', self.changelog)
        self.config_obj.set(
            'general', 'deprecated', self.deprecated)
        self.config_obj.set(
            'general', 'description', self.description)
        self.config_obj.set(
            'general', 'email', self.email)
        self.config_obj.set(
            'general', 'experimental', self.experimental)
        self.config_obj.set(
            'general', 'hasProcessingProvider',
            self.has_processing_provider)
        self.config_obj.set(
            'general', 'homepage', self.homepage)
        self.config_obj.set(
            'general', 'icon', self.icon)
        self.config_obj.set(
            'general', 'name', self.name)
        self.config_obj.set(
            'general', 'plugin_dependencies', self.plugin_dependencies)
        self.config_obj.set(
            'general', 'qgisMaximumVersion', self.qgis_maximum_version)
        self.config_obj.set(
            'general', 'qgisMinimumVersion', self.qgis_minimum_version)
        self.config_obj.set(
            'general', 'repository', self.repository)
        self.config_obj.set(
            'general', 'tags', ', '.join(self.tags))
        self.config_obj.set(
            'general', 'tracker', self.tracker)
        self.config_obj.set(
            'general', 'version', self.version)
        return True

    def read_metadata(self, in_file):
        """ Reads the metadata.txt file. """
        with open(in_file, 'w') as fin:
            self.config_obj.read_file(fin)

        self.about = self.config_obj.get(
            'general', 'about', fallback=self.about)
        self.author = self.config_obj.get(
            'general', 'author', fallback=self.author)
        self.category = self.config_obj.get(
            'general', 'category', fallback=self.category)
        self.changelog = self.config_obj.get(
            'general', 'changelog', fallback=self.changelog)
        self.deprecated = self.config_obj.get(
            'general', 'deprecated', fallback=self.deprecated)
        self.description = self.config_obj.get(
            'general', 'description', fallback=self.description)
        self.email = self.config_obj.get(
            'general', 'email', fallback=self.email)
        self.experimental = self.config_obj.get(
            'general', 'experimental', fallback=self.experimental)
        self.has_processing_provider = self.config_obj.get(
            'general', 'hasProcessingProvider',
            fallback=self.has_processing_provider)
        self.homepage = self.config_obj.get(
            'general', 'homepage', fallback=self.homepage)
        self.icon = self.config_obj.get(
            'general', 'icon', fallback=self.icon)
        self.name = self.config_obj.get(
            'general', 'name', fallback=self.name)
        self.plugin_dependencies = self.config_obj.get(
            'general', 'plugin_dependencies', fallback=self.plugin_dependencies)
        self.qgis_maximum_version = self.config_obj.get(
            'general', 'qgisMaximumVersion', fallback=self.qgis_maximum_version)
        self.qgis_minimum_version = self.config_obj.get(
            'general', 'qgisMinimumVersion', fallback=self.qgis_minimum_version)
        self.repository = self.config_obj.get(
            'general', 'repository', fallback=self.repository)
        self.tags = [tag.trim for tag in self.config_obj.get(
            'general', 'tags', fallback=', '.join(self.tags)).split(',')]
        self.tracker = self.config_obj.get(
            'general', 'tracker', fallback=self.tracker)
        self.version = self.config_obj.get(
            'general', 'version', fallback=self.version)

    def write_metadata(self, out_file):
        """ Writes the metadata.txt file. """
        if not self.to_metadata():
            return

        with open(out_file, 'w') as fout:
            self.config_obj.write(fout)

    def parse_init(self, init_path):
        """
        Reads the modules imported by a package init file.

        Arguments:
            init_path (str):
                The path of the __init__ file.

        Returns:
            The list of modules detected inside the file.
        """
        b_inside = False
        modules =[]
        with open(init_path, 'r') as fin:
            for line in fin:
                line = line.strip()
                if 'classFactory' in line:
                    b_inside = True
                elif b_inside:
                    if line.startswith('from ') and ' import ' in line:
                        modules.append(line[5:line.find(' import ')].strip())
        return modules

    def load_modules(self, path, modules, source_py):
        """
        Creates modules instances and reads their files.

        Attributes:
            path (str):
                The path of the package.
            modules (list):
                A list of module names.

        Returns:
            A list of PubModule instances.
        """
        result = []
        for module_name in modules:
            m = PubModule(
                    name=module_name, path=os.path.join(path, module_name))
            m.collect_py_files(source_py=source_py)
            result.append(m)
        return result

    def load_extra_files(self, path):
        """
        Creates modules instances and reads their files.

        Attributes:
            path (str):
                The path of the package.

        Returns:
            A list of files.
        """
        result = []
        include_files = self.config_obj.get('extra', 'files', fallback='')
        include_dirs = self.config_obj.get('extra', 'directories', fallback='')

        for file in include_files.split("\n"):
            file = os.path.join(path, file.strip())
            if os.path.isfile(file):
                result.append(file)
            else:
                logger.error("Extra file does not exist: %s", file)

        for directory in include_dirs.split("\n"):
            file = os.path.join(path, directory.strip())
            if os.path.isdir(file):
                for root, dirs, files in os.walk(".", topdown=False):
                    for name in files:
                        result.append(os.path.join(root, name))
            else:
                logger.error("Extra directory does not exist: %s", file)

        return result

    def load_ui_files(self, path):
        """
        Finds ui files.

        Attributes:
            path (str):
                The path of the package.

        Returns:
            A list of files.
        """
        result = []
        include_ui = self.config_obj.get('extra', 'ui', fallback='')

        for file in include_ui.split("\n"):
            file = os.path.join(path, file.strip())
            if os.path.isfile(file):
                result.append(file)
            elif os.path.isdir(file):
                for ui_file in os.listdir(file):
                    if ui_file.endswith('.ui') or ui_file.endswith('.UI'):
                        result.append(PubUi(os.path.join(file, ui_file)))
            else:
                logger.error("Extra file does not exist: %s", file)

        return result

    def load_qrc_files(self, path):
        """
        Finds ui files.

        Attributes:
            path (str):
                The path of the package.

        Returns:
            A list of files.
        """
        result = []
        include_ui = self.config_obj.get('extra', 'qrc', fallback='')

        for file in include_ui.split("\n"):
            file = os.path.join(path, file.strip())
            if os.path.isfile(file):
                result.append(file)
            elif os.path.isdir(file):
                for ui_file in os.listdir(file):
                    if ui_file.endswith('.qrc') or ui_file.endswith('.QRC'):
                        result.append(PubQrc(os.path.join(file, ui_file)))
            else:
                logger.error("Extra file does not exist: %s", file)

        return result

    def collect_files_to_deploy(self):
        """ Creates a single list of all files to be copied. """
        result = []
        for module in self.modules:
            result.extend(module.files)
        result.extend(self.extra_files)
        for ui_file in self.ui_files:
            result.append(ui_file.path_out)
        for qrc_file in self.qrc_files:
            result.append(qrc_file.path_out)
        return result

    def deploy(self, target):
        """
        Copies files to target directory.

        Arguments:
            target (str):
                A directory path.
        """
        if not os.path.isdir(target):
            os.makedirs(target)

        for file in self.collect_files_to_deploy():
            shutil.copy()
