import os

from ExtensionClass import Base

class MultiMapping(Base):
    __slots__ = ('__dicts__',)

    def __init__(self, *args):
        self.__dicts__ = list(args)

    def __getitem__(self, key):
        for d in self.__dicts__[::-1]:
            try:
                return d[key]
            except (KeyError, AttributeError):
                # XXX How do we get an AttributeError?
                pass
        raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def has_key(self, key):
        try:
            self[key]
        except KeyError:
            return False
        return True

    def push(self, d):
        self.__dicts__.append(d)

    def pop(self, n=-1):
        return self.__dicts__.pop(n)

    def __len__(self):
        return sum(len(d) for d in self.__dicts__)

pyMultiMapping = MultiMapping

if 'PURE_PYTHON' not in os.environ:  # pragma no cover
    try:
        from _MultiMapping import *  # noqa
    except ImportError:
        pass
