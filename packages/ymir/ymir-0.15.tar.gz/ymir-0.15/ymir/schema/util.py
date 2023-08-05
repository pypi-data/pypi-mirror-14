# -*- coding: utf-8 -*-
""" ymir.schema.util
"""
from voluptuous import Invalid  # Required, Optional, Undefined


def list_of_dicts(lst, key=None):
    """ """
    if not isinstance(lst, list):
        err = ("expected list of strings for key @ `{0}`")
        err = err.format(key or 'unknown')
        raise Invalid(err)
    for i, x in enumerate(lst):
        if not isinstance(x, dict):
            err = ('expected JSON but top[{0}][{1}] is {2}')
            err = err.format(key, i, type(x))
            raise Invalid(err)


def list_of_strings(lst, key=None):
    if not isinstance(lst, list):
        err = ("expected list of strings for key @ `{0}`, got {1}")
        err = err.format(key or 'unknown', str(list))
        raise Invalid(err)
    for i, x in enumerate(lst):
        if not isinstance(x, basestring):
            print lst
            err = (
                'expected string for key@`{0}`, but index {1} is "{3}" of type {2}')
            err = err.format(
                key, i, type(x).__name__, x)
            raise Invalid(err)
