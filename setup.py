# -*- coding: utf-8 -*-
########################################################################
#
#       License: BSD 3-clause
#       Created: September 22, 2010
#       Author:  Francesc Alted - faltet@gmail.com
#
########################################################################

# flake8: noqa

from __future__ import print_function

import os
import sys

from skbuild import setup

# Workaround to ensure cpuinfo can be imported using latest pip.
# For more details, see https://github.com/pypa/pip/issues/6163
sys.path.insert(0, os.path.dirname(__file__))
import cpuinfo


# ########## Check versions ##########
def exit_with_error(message):
    print('ERROR: %s' % message)
    sys.exit(1)


# Check for Python
if sys.version_info[0] == 2:
    if sys.version_info[1] < 7:
        exit_with_error("You need Python 2.7 or greater to install blosc!")
elif sys.version_info[0] == 3:
    if sys.version_info[1] < 4:
        exit_with_error("You need Python 3.4 or greater to install blosc!")
else:
    exit_with_error("You need Python 2.7/3.4 or greater to install blosc!")

tests_require = ['numpy']

# ########## End of checks ##########

# Read the long_description from README.rst
with open('README.rst') as f:
    long_description = f.read()

# Blosc version
VERSION = open('VERSION').read().strip()
# Create the version.py file
open('blosc/version.py', 'w').write('__version__ = "%s"\n' % VERSION)


# Global variables
# CFLAGS = os.environ.get('CFLAGS', '').split()
# LFLAGS = os.environ.get('LFLAGS', '').split()

# Handle --blosc=[PATH] --lflags=[FLAGS] --cflags=[FLAGS]
# args = sys.argv[:]
# for arg in args:
#     if arg.find('--blosc=') == 0:
#         BLOSC_DIR = os.path.expanduser(arg.split('=')[1])
#         sys.argv.remove(arg)
#     if arg.find('--lflags=') == 0:
#         LFLAGS = arg.split('=')[1].split()
#         sys.argv.remove(arg)
#     if arg.find('--cflags=') == 0:
#         CFLAGS = arg.split('=')[1].split()
#         sys.argv.remove(arg)

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: Information Technology
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Topic :: Software Development :: Libraries :: Python Modules
Topic :: System :: Archiving :: Compression
Operating System :: Microsoft :: Windows
Operating System :: Unix
"""

cpu_info = cpuinfo.get_cpu_info()


def cmake_bool(cond):
    return 'ON' if cond else 'OFF'


setup(name = "blosc",
      version = VERSION,
      description = 'Blosc data compressor',
      long_description = """\

Blosc is a high performance compressor optimized for binary data.

""",
      classifiers = [c for c in classifiers.split("\n") if c],
      author = 'Francesc Alted, Valentin Hänel',
      author_email = 'faltet@gmail.com, valentin@haenel.co',
      maintainer = 'Francesc Alted',
      maintainer_email = 'faltet@gmail.com',
      url = 'http://github.com/blosc/python-blosc',
      license = 'https://opensource.org/licenses/BSD-3-Clause',
      platforms = ['any'],
      cmake_args = [
          '-DBLOSC_DIR:PATH=%s' % os.environ.get('BLOSC_DIR', ''),
          '-DDEACTIVATE_SSE2:BOOL=%s' % cmake_bool('DISABLE_BLOSC_SSE2' in os.environ or 'sse2' not in cpu_info['flags']),
          '-DDEACTIVATE_AVX2:BOOL=%s' % cmake_bool('DISABLE_BLOSC_AVX2' in os.environ),
          '-DDEACTIVATE_LZ4:BOOL=%s' % cmake_bool(not int(os.environ.get('INCLUDE_LZ4', '1'))),
          # Snappy is disabled by default
          '-DDEACTIVATE_SNAPPY:BOOL=%s' % cmake_bool(not int(os.environ.get('INCLUDE_SNAPPY', '0'))),
          '-DDEACTIVATE_ZLIB:BOOL=%s' % cmake_bool(not int(os.environ.get('INCLUDE_ZLIB', '1'))),
          '-DDEACTIVATE_ZSTD:BOOL=%s' % cmake_bool(not int(os.environ.get('INCLUDE_ZSTD', '1'))),
      ],
      tests_require=tests_require,
      packages = ['blosc'],
)
