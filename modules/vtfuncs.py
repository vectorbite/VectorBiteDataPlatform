#!/bin/env python
# -*- coding: utf-8 -*-

"""
vtfuncs.py
Author: Francis Windram
Created: 27/03/19
Docstr: This file contains many generic VecTraits functions with which to perform validation and other jobs
"""

import logging

logger = logging.getLogger("web2py.app.vbdp")
logger.setLevel(logging.DEBUG)


def listtodict(h, l):
    """
    Convert a set of two lists to a dictionary

        >>> listtodict(["test1", "test2"], [1, 2])
        {'test1': 1, 'test2': 2}

    """
    try:
        return dict(zip(h, l))
    except TypeError:
        raise TypeError("Both headers and values must be in list format")


def data_to_dicts(h, d):
    """
    Convert a list of lists to a list of dicts given a header list

        >>> data_to_dicts(["test1", "test2"], [[1,2], [3,4]])
        [{'test1': 1, 'test2': 2}, {'test1': 3, 'test2': 4}]

        >>> data_to_dicts(["test1", "test2"], [[1,2], [3]])
        [{'test1': 1, 'test2': 2}, {'test1': 3}]

    """
    return [listtodict(h, x) for x in d]
