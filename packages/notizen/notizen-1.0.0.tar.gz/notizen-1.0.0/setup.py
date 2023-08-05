# coding: utf-8
'''
setup.py

Reference: https://packaging.python.org/en/latest/distributing/
'''


import sys
from setuptools import (setup, Command)
from setuptools.command.test import test as TestCommand
from notizen import (
    __version__, __license__, __url__,
    __program_name__, __short_description__,
    __main_author_name__, __main_author_email__
)


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('README.rst') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name=__program_name__,
    version=__version__,
    description=__short_description__,
    license=__license__,
    author=__main_author_name__,
    author_email=__main_author_email__,
    url=__url__,
    # FIXME download_url, maintainer, maintainer_email, py_modules
    # during setup.py wheel==0.26.0 was installed for bdist_wheel
    # scripts=['bin/notizen'],  # FIXME point to cli.py:cli()
    # Via `PyPackage/pybuild -isN`:
    classifiers=[ 
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Artistic Software',
        'Topic :: Documentation',
        'Topic :: Utilities'
    ],
    packages=['notizen',],
    long_description=long_description,
    keywords=['notes', 'index', 'search', 'documentation'],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    zip_safe=True,
    entry_points={
        'console_scripts': [ 'notizen=notizen.cli:main']
    },
)
