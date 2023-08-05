# :coding: utf-8
# :copyright: Copyright (c) 2016 Martin Pengelly-Phillips

import os
import re

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.join(ROOT_PATH, 'source')
README_PATH = os.path.join(ROOT_PATH, 'README.rst')

# Read version from source.
with open(os.path.join(
    SOURCE_PATH, 'flattener', '_version.py')
) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)


# Custom commands.
class PyTest(TestCommand):
    '''Pytest command.'''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        '''Import pytest and run.'''
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


# Configuration.
setup_requires = [
    'sphinx >= 1.2.2, < 2',
    'sphinx_rtd_theme >= 0.1.6, < 2',
    'lowdown >= 0.1.0, < 2'
]

install_requires = [
]

# Readthedocs requires Sphinx extensions to be specified as part of
# install_requires in order to build properly.
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    install_requires.extend(setup_requires)


setup(
    name='Flattener',
    version=VERSION,
    description='Flatten lists of lists.',
    long_description=open(README_PATH).read(),
    keywords='array, list, flatten',
    url='https://github.com/martinpengellyphillips/flattener',
    author='Martin Pengelly-Phillips',
    author_email='martin@4degrees.ltd.uk',
    license='Apache License (2.0)',
    packages=find_packages(SOURCE_PATH),
    package_dir={
        '': 'source'
    },
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=[
        'pytest >= 2.3.5, < 3'
    ],
    cmdclass={
        'test': PyTest
    },
    zip_safe=False
)
