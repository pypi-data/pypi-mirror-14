# -*- coding: utf-8 -*-

"""Map Depot Indexer.

Command Line Interface Module
"""

from __future__ import absolute_import
import click
import os
import json
from mapdepot.schemas import Topographic


@click.command()
@click.argument('command')
@click.option('--path', default='.', help='Path to index')
@click.option('--filetypes', default=['.jpeg', '.tif'], help='File types')
@click.option('-v', '--verbose', count=True)
def cli(command, **kwargs):
    """Command Line Interface."""
    if command in ['index']:
        index(**kwargs)


def index(**kwargs):
    """Indexer."""
    for dirpath, dirnames, filenames in os.walk(kwargs['path']):
        for filename in filenames:
            if filename.endswith(tuple(kwargs['filetypes'])):
                topographic = Topographic(os.path.join(dirpath, filename))
                results = topographic.json
                if kwargs['verbose']:
                    click.echo(json.dumps(results))

if __name__ == '__main__':
    cli()
