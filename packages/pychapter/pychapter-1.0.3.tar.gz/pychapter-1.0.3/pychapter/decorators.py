#!/usr/bin/env python3
"""
    Decorators
"""
from contextlib import suppress


def cached(func):
    """
        Returns a list, with each entry that matches
        a key in the extra_info list of dicts.

        This only applies to general series info.
    """
    def inner(*args, **kwargs):
        """ Decorator """
        with suppress(AttributeError):
            result = getattr(args[0], "_{}".format(func.__name__))
            if result:
                return result

        setattr(args[0], "_{}".format(func.__name__), func(*args, **kwargs))
        return getattr(args[0], "_{}".format(func.__name__))

    return inner
