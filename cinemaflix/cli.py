#!/usr/bin/env python

import os
import sys

from main import TSearch


def cli():
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
