__author__ = 'dpepper'
__version__ = '0.1.0'


import os
import sys


def realpath(path):
    return os.path.realpath(path)


def main():
    args = sys.argv[1:] or '.'

    for path in args:
        print path
