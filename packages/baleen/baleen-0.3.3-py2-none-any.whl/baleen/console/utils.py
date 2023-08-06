# baleen.console.utils
# Argparse extensions and utilities.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Mar 02 11:01:35 2016 -0500
#
# Copyright (C) 2016 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: utils.py [da54aa8] benjamin@bengfort.com $

"""
Argparse extensions and utilities.
"""

##########################################################################
## Imports
##########################################################################

import argparse


##########################################################################
## Console Parsers
##########################################################################

def csv(ptype=int):
    """
    Argparse type for comma seperated values. Also parses the type, e.g. int.
    """
    def parser(s):
        try:
            parse = lambda p: ptype(p.strip())
            return map(parse, s.split(","))
        except Exception:
            raise argparse.ArgumentTypeError(
                "Could not parse CSV value to type {}: {!r}".format(ptype.__name__, s)
            )

    return parser
