"""
Memoizing decorators
"""
from __future__ import print_function
from collections import deque
import time

from builtins import next
from builtins import object


class memoize(object):
    """
    Memoize results of function calls
    """

    def __init__(self, function):
        """
        """
        self.function = function
        self.cache = {}

    def __call__(self, *args, **kw):
        if kw:  # frozenset is used to ensure hashability
            key = args, frozenset(list(kw.items()))
        else:
            key = args
        if key not in self.cache:
            self.cache[key] = self.function(*args, **kw)
        return self.cache[key]

class memoizeFor(object):
    """
    Memoize results of a function for a certain time
    """

    def __init__(self, cachetime):
        self.cachetime = cachetime

    def __call__(self, function):
        cache = {}
        def wrapped(*args, **kw):
            if kw:
                key = args, frozenset(list(kw.items()))
            else:
                key = args
            # Clean cache
            time_ = time.time()
            ctime = int(time_ - self.cachetime)
            for k, (vtime, value) in list(cache.items()):
                if vtime < ctime:
                    del cache[k]
            if key in cache:
                return cache[key][1]
            else:
                result = function(*args, **kw)
                cache[key] = time_, result
                return result
        return wrapped

class memoizeUpto(object):
    """
    Memoize results of a function upto a certain limit

    Using a deque, the cache size is limited automatically
    """
    class _boxed(object):
        def __init__(self, value):
            self.value = value

    def __init__(self, maxsize=256):
        """
        Create object

        :param int maxsize: maximum cache size (default 256)
        """
        self.maxsize = maxsize

    def __call__(self, function):
        cache = None
        def wrapped(*args, **kw):
            if kw:
                key = args, frozenset(list(kw.items()))
            else:
                key = args
            try:
                result = next(v for k, v in cache if k == key)
            except StopIteration:
                result = function(*args, **kw)
                cache.append((key, result))
            return result
        cache = deque(maxlen=self.maxsize)
        return wrapped
