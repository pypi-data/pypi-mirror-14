#!/usr/bin/env python3
"""
    Decorators
"""
from contextlib import suppress
from guessit import guessit
from . info_providers import search_info

def series_info(func):
    """
        Returns a list, with each entry that matches
        a key in the extra_info list of dicts.

        This only applies to general series info.
    """
    def inner(*args, **kwargs):
        """ Decorator """

        def get_for_name(name):
            with suppress(AttributeError):
                return getattr(args[0], "_{}".format(name))

            result = []
            for info in getattr(args[0], '_extra_info'):
                with suppress(KeyError):
                    result.append(info[name])
                setattr(args[0], "_{}".format(name),
                        result)

            with suppress(AttributeError):
                return getattr(args[0], "_{}".format(name))

        if not hasattr(args[0], '_extra_info'):
            info = search_info(args[0].title, args[0].season,
                               args[0].episode)
            setattr(args[0], '_extra_info', list(info))

        return [get_for_name(name) for name in func(*args, **kwargs)]

    return inner


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
