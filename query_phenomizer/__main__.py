#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
query_phenomizer.__main__
~~~~~~~~~~~~~~~~~~~~~

The main entry point for the command line interface.

Invoke as ``query_phenomizer`` (if installed)
or ``python -m query_phenomizer`` (no install required).
"""
import sys

from .cli import cli


if __name__ == '__main__':
    # exit using whatever exit code the CLI returned
    sys.exit(cli())
