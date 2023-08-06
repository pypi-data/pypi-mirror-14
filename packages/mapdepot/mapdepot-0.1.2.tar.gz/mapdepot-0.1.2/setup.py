# -*- coding: utf-8 -*-
"""Map Depot Indexer.

Command Line Interface Module
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt') as f:
    REQUIRES = f.readlines()

setup(
    name='mapdepot',
    version='0.1.2',
    description='Map Depot\'s helpful scripts for indexing their data.',
    packages=['mapdepot', 'mapdepot.schemas'],
    install_requires=[REQUIRES],
    entry_points={
        'console_scripts': [
            'mapdepot = mapdepot.cli:cli'
        ]
    }
)
