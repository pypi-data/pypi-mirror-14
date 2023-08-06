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

    Args:
        root (dict|list): The root item

    Returns:
        The dotable representation.
    """

    def __new__(cls, root):
        if isinstance(root, dict):
            return DotableDict(root)
        elif isinstance(root, list):
            return DotableList(root)
        else:
            raise ValueError('The root item must be a list or dict')
