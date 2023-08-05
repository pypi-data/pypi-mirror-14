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
