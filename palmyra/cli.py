#!/usr/bin/env python
#walid.saad

from main import TSearch
import sys
import os

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