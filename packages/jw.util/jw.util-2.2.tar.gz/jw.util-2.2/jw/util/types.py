"""
Type helpers
"""
from itertools import chain

def Args2Str(*args, **kwargs):
    """
    Convert arguments and keyword arguments to a string

    :param tuple args:
    :param dict kwargs:
    :return: string denoting arguments and keyword arguments
    :rtype: str
    """
    return ', '.join(chain((repr(arg) for arg in args), ('%s=%s' % (k, v) for k, v in kwargs.items())))


def Abbr(obj, length=128):
    """
    Abbreviates string representation of object

    :param object obj:
    :param int length: maximum length

    Converts `obj` to string and returns the first `length` characters plus an ellipsis if it is longer than `length` or
    just the string representation.
    """
    srep = obj.decode('utf-8') if isinstance(obj, bytes) else str(obj)
    return srep[:length] + '...' if len(srep) > length else srep
