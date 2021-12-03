# -*- coding: utf-8 -*-

"""
Allow calling 2ip CLI as a Python module

This allows the CLI to be called like this:

    python3 -m twoip ...
"""
if __name__ == '__main__':
    from twoip.cli import cli
    cli()