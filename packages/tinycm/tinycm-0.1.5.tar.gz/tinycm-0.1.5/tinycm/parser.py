import ruamel.yaml
import requests
import tempfile
import os
import re
import importlib
import urllib.parse
import logging
import boolexp

from tinycm import UndefinedTypeError


class CMParser(object):
    def __init__(self, input_file, hostname, name=None, module_path=None, tempdir=None, arguments=None):
        if not tempdir:
            self.tempdir = tempfile.mkdtemp(prefix='tinycm-')
        if not name:
            self.name = 'rootfile'

        self.source = input_file
        self.source_type = 'file'
        self.module_path = module_path
        if input_file.startswith('http://') or input_file.startswith('https://'):
            logging.info('Downloading {}'.format(input_file))
            response = requests.get(input_file)
            filename = os.path.join(self.tempdir, self.name)
            with open(filename, 'wb') as target_file:
                target_file.write(response.content())

            self.filename = filename
            self.source_type = 'http'
            logging.debug('Download complete')
        else:
            logging.info('Processing {}'.format(input_file))
            self.filename = input_file
        logging.debug('Actual input file: {}'.format(self.filename))
        self.hostname = hostname
        self.hosts = {}
        self.constants = {}
        self.definitions = {}

        if arguments:
            self.constants = arguments

        self._parse()

    def _parse(self):
        self.raw = ruamel.yaml.safe_load_all(open(self.filename))
        frontmatter = self.raw.__next__()

        if 'arguments' in frontmatter:
            # This is a module
            logging.info('Input file is a module')
            constants = frontmatter['arguments']
            constants.update(self.constants)
            self.constants = constants
        else:
            # This is a configuration definition
            logging.info('Input file is a configuration file')
            if 'global' in frontmatter:
                logging.debug('Global constants imported')
                self.constants = frontmatter['global']

            if 'hosts' in frontmatter:
                for host in frontmatter['hosts']:
                    logging.debug('Matching hostname "{}" on regex {}'.format(self.hostname, host['filter']))
                    if re.match(host['filter'], self.hostname):
                        logging.info('Host filter {} matched'.format(host['filter']))
                        self.constants.update(host['constants'])

        for definition in self.raw:
            self._load_definition(definition)

    def _load_definition(self, definition):
        definition_type = list(definition.keys())[0]
        definition = definition[definition_type]
        if 'if' in definition:
            result = self._process_definition_if(definition)
            if not result:
                return
        if isinstance(definition['name'], list):
            for name in definition['name']:
                d = definition.copy()
                d['name'] = name
                self._insert_definition(definition_type, name, d)
        else:
            self._insert_definition(definition_type, definition['name'], definition)

    def _process_definition_if(self, definition):
        logging.info('Evalueating expression {}'.format(definition['if']))
        for key in self.constants:
            logging.debug('  {} = {}'.format(key, repr(self.constants[key])))
        expr = boolexp.Expression(definition['if'])
        result = expr.evaluate(self.constants)
        logging.debug('Expression evaluated to: {}'.format(result))
        return result

    def _insert_definition(self, type, name, parameters):
        if type == 'import':
            logging.info('Parsing import definition')
            import_name = self._get_import_name(name)
            import_parsed = CMParser(import_name, self.hostname, name, self.module_path, self.tempdir, parameters)
            for identifier in import_parsed.definitions:
                if identifier in self.definitions:
                    self.definitions[identifier] = self.definitions[identifier].try_merge(
                            import_parsed.definitions[identifier])
                else:
                    self.definitions[identifier] = import_parsed.definitions[identifier]
            return
        identifier = '{}::{}'.format(type, name)
        module_name = 'tinycm.definitions.{}'.format(type)
        logging.debug('Checking for module existence: {}'.format(module_name))

        try:
            module = importlib.import_module(module_name)
        except ImportError:
            try:
                module_name = 'tinycm_{}'.format(type)
                module = importlib.import_module(module_name)
            except ImportError:
                raise UndefinedTypeError("Type not found: {}".format(type))

        class_name = '{}Definition'.format(type.title())
        class_ = getattr(module, class_name)

        after = []
        if 'after' in parameters:
            if isinstance(parameters['after'], list):
                after = parameters['after']
            else:
                after = [parameters['after']]

        logging.debug('Creating instance of {}'.format(class_name))
        instance = class_(identifier, parameters, self.source, after, self.constants)

        if hasattr(instance, 'dependencies'):
            deps = instance.dependencies()
            for dep in deps:
                self._insert_definition(dep.type, dep.name, dep.parameters)

        if identifier in self.definitions:
            logging.info('Duplicate definition found ({}), trying merge'.format(identifier))
            self.definitions[identifier] = self.definitions[identifier].try_merge(instance)
        else:
            self.definitions[identifier] = instance

    def _get_import_name(self, name):
        if self.module_path.startswith('http://') or self.module_path.startswith('https://'):
            parts = urllib.parse.urlparse(self.module_path)
            path = os.path.join(parts.path, '{}.mod.yml'.format(name))
            parts.path = path
            return urllib.parse.urlunparse(parts)
        else:
            return os.path.join(self.module_path, '{}.mod.yml'.format(name))
