#!/usr/bin/env python

import argparse
import os
import sys

from cinemaflix import __version__
from main import TSearch


def cli():
    parser = argparse.ArgumentParser(usage='-h for full usage')
    parser.add_argument(
        '-V', '--version', action='version', version=__version__)
    parser.parse_args()
    try:
        TSearch().main()
    except KeyboardInterrupt:
        print '\nExiting...'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == '__main__':
    cli()
