#!/usr/bin/env python

# Copyright 2017-2020 Palantir Technologies, Inc.
# Copyright 2021- Python Language Server Contributors.

import ast
import os
from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='pylsp_jsonrpc'):
    """Get version."""
    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()
    lines = data.split('\n')
    for line in lines:
        if line.startswith('VERSION_INFO'):
            version_tuple = ast.literal_eval(line.split('=')[-1].strip())
            version = '.'.join(map(str, version_tuple))
            break
    return version


README = open('README.md', 'r').read()


setup(
    name='python-lsp-jsonrpc',
    version=get_version(),
    description='JSON RPC 2.0 server library',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/python-lsp/python-lsp-jsonrpc',
    author='Python Language Server Contributors',
    packages=find_packages(exclude=['contrib', 'docs', 'test']),
    install_requires=[
        'ujson>=3.0.0',
    ],
    extras_require={
        'test': ['pylint', 'pycodestyle', 'pyflakes', 'pytest',
                 'pytest-cov', 'coverage'],
    },
)
