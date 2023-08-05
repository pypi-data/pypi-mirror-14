import sys
import os

from codecs import open

from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-arg=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        sys.exit(pytest.main(self.pytest_args))


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.rst', 'r', 'utf-8') as f:
    README = f.read().strip()

with open('LICENSE', 'r', 'utf-8') as f:
    LICENSE = f.read().strip()

with open('HISTORY.rst', 'r', 'utf-8') as f:
    HISTORY = f.read().strip()

requires = [
    'pymongo'
]

setup(name='rcquerybuilder',
      version='0.1.2',
      url='http://github.com/red-crown/mongo-querybuilder/',
      description='Provides a fluent query builder wrapper around pymongo',
      long_description=README + '\n\n' + HISTORY,
      author='Matthew Strickland',
      author_email='matthew@redcrown.co',
      license=LICENSE,
      tests_require=['pytest', 'pytest-cov'],
      platforms='any',
      zip_safe=False,
      package_data={'': ['LICENSE', 'README.rst', 'HISTORY.rst']},
      package_dir={'rcquerybuilder': 'rcquerybuilder'},
      include_package_data=True,
      install_requires=requires,
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Database'
      ],
      packages=find_packages(exclude=('tests', 'docs')),
      cmdclass={'test': PyTest})
