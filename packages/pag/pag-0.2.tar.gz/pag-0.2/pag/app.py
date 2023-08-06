#!/usr/bin/env python

import click

@click.group()
def app():
    pass

__all__ = [
    'app',
]

from .commands import create
from .commands import clone
from .commands import remote


if __name__ == '__main__':
    app()
