# encoding: utf8

# pyinfra
# File: pyinfra/facts/npm.py
# Desc: npm package manager facts

from pyinfra.api import FactBase

from .util.packaging import parse_packages

# Matching output of npm list
npm_regex = ur'^[└├]\─\─\s([a-zA-Z0-9\-]+)@([0-9\.]+)$'


class NpmPackages(FactBase):
    '''
    Returns a dict of globally installed npm packages:

    .. code:: python

        'package_name': 'version',
        ...
    '''

    command = 'npm list -g --depth=0'

    @classmethod
    def process(cls, output):
        parse_packages(npm_regex, output)


class NpmLocalPackages(FactBase):
    '''
    Returns a dict of locally installed npm packages in a given directory:

    .. code:: python

        'package_name': 'version',
        ...
    '''

    @classmethod
    def command(cls, directory):
        return 'cd {0} && npm list -g --depth=0'.format(directory)

    @classmethod
    def process(cls, output):
        parse_packages(npm_regex, output)
