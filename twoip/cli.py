# -*- coding: utf-8 -*-

"""
CLI interface for 2ip.me
"""

# Import requirements
from os import path
from typing import Optional

# Import logging
import logging as l

# Import 2ip module
from .twoip import TwoIP

# Set default path to the API key file to check for to ~/.config/2ip.key
_key = path.join(path.expanduser('~'), '.config', '2ip.key')

class cli(object):

    # Import click to parse CLI args
    import click

    # Get command line arguments
    @click.command()
    @click.option(
        '-k', '--key', 'key',
        default         = _key,
        help            = 'An optional file containing the API key.',
        show_default    = True,
        type            = click.Path(exists = False, dir_okay = False, readable = True),
    )
    @click.option(
        '-v', '--verbose', 'verbosity',
        count   = True,
        help    = 'Set logging level.',
    )
    @click.option(
        '-a', '--action', 'action',
        default         = 'run',
        help            = 'The action to perform.',
        show_default    = True,
        type            = click.Choice(['run', 'monitor'], case_sensitive = False),
    )

    def __init__(self, key: Optional[str], verbosity: Optional[int], action: Optional[str]):
        print('test')

if __name__ == '__main__':
    #twoip = cli()
    print('test')