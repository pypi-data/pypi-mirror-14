#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
import sys

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

if float('%d.%d' % sys.version_info[:2]) < 2.6 or float('%d.%d' % sys.version_info[:2]) >= 3.0:
    sys.stderr.write("Your Python version %d.%d.%d is not supported.\n" %
                     sys.version_info[:3])
    sys.stderr.write("OAS Python SDK requires Python between 2.6 and 3.0.\n")
    sys.exit(1)

classifiers = [
    'Development Status :: 4 - Beta',

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',

    'Operating System :: OS Independent',

    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
]

setup(
    name='oassdk',
    version='0.2.5',
    description='Python SDK for Aliyun OAS (Open Archive Service)',
    author='Aliyun OAS',
    author_email='jianyi.weng@alibaba-inc.com',
    url='http://www.aliyun.com/product/oas',
    packages=['oas', 'oas.ease'],
    license='GPL version 2',
    install_requires=[
        'pyaml',
        'ordereddict',
    ],
    scripts=['oascmd.py'],
)
