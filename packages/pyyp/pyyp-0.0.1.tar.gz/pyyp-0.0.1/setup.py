#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pyyp

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

required = ['requests>=2.0.0']


setup(
    name='pyyp',
    version=pyyp.__version__,
    description='Yunpian API wrapper.',
    long_description=open('README.md').read(),
    author='Kent Wang',
    author_email='pragkent@gmail.com',
    url='https://github.com/pragkent/pyyp',
    packages=['pyyp'],
    package_data={'': ['LICENSE',]},
    include_package_data=True,
    install_requires=required,
    license='MIT',
    classifiers=(
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ),
)
