#!/usr/bin/env python

import os
import sys

from main import TSearch


def cli():
    TSearch().main()

if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print '\nExiting...'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
