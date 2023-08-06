# -*- coding: utf-8 -*-
import sys


class DotableDict(dict):

    __getattr__ = dict.__getitem__

    def __init__(self, d):
        if sys.version_info >= (3,):
            self.update(**dict((k, self.parse(v)) for k, v in d.items()))  # in py3 use .items
        else:
            self.update(**dict((k, self.parse(v)) for k, v in d.iteritems()))

    @classmethod
    def parse(cls, v):
        if isinstance(v, dict):
            return cls(v)
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v


class DotableList(list):

    def __init__(self, l):
        for item in l:
            self.append(self.parse(item))

    @classmethod
    def parse(cls, v):
        if isinstance(v, dict):
            return DotableDict(v)
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v


class Dotable(object):
    """Parse a dictionary or list into the equivalent dot notation.

    It will parse the first dict or list item in the arguments. A list or dict
    must be present somewhere in the args list.

    Returns:
        The dotable representation of the first compatible arg in the list.
    """
    def __new__(cls, *args, **kwargs):
        for arg in args:
            if isinstance(arg, dict):
                return DotableDict(arg)
            elif isinstance(arg, list):
                return DotableList(arg)
        raise ValueError('One of the arguments must be a list or dict')
