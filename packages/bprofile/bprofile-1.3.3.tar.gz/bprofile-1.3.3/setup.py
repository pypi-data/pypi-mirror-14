#!/usr/bin/env python

# To upload a version to PyPI, run:
#    python setup.py sdist upload
# If the package is not registered with PyPI yet, do so with:
#     python setup.py register

from distutils.core import setup
import os

__version__ = '1.3.3'

DESCRIPTION = \
    """A wrapper around profile/cProfile, gprof2dot and dot,
providing a simple context manager for profiling sections
of Python code and producing visual graphs of profiling results."""

# Auto generate a __version__ module for the package to import
with open(os.path.join('bprofile', '__version__.py'), 'w') as f:
    f.write("__version__ = '%s'\n" % __version__)

# Ensure graphviz is installed:
from bprofile.bprofile import DOT_PATH

setup(name='bprofile',
      version=__version__,
      description=DESCRIPTION,
      author='Chris Billington',
      author_email='chrisjbillington@gmail.com',
      url='https://bitbucket.org/cbillington/bprofile',
      license="simplified BSD",
      packages=['bprofile'],
      classifiers=[
        # See: https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Benchmark',
        'Topic :: Utilities',
      ])
