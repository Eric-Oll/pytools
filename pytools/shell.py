# -*- coding: utf-8 -*-

"""This module provides a several function useful in shell"""
import sys
import os


def head(file='', lines=10, output=sys.stdout):
    """
    Print in the stdin the <lines> first lines of file <file>
    """

    try:
        with open(file, 'r') as fd:
            for i in range(lines):
                print(fd.readline(), end='', file=output)
    except EOFError:
        print('<End of file>')
        
    except Exception as err:
        print(err, file=sys.stderr)
        
