"""
Extension stuff
"""
from __future__ import absolute_import
from builtins import next

# TODO: documentation

from .memoize import memoize
from pkg_resources import iter_entry_points

class ResourceNotFound(RuntimeError):
    """
    Resource was not found
    """

class ResourceNotUnique(RuntimeError):
    """
    More than one resource found for condition
    """

@memoize
def Load(namespace, name):
    """
    Load a resource fromo entry points accrding to conditions

    :type namespace: str
    :type name: str
    :return: resource
    :rtype: object
    :raise ResourceNotFound: if no resource was found

    .. note::
       Only the first resource is returned, if if more than one are found
    """
    try:
        return next(iter_entry_points(namespace, name)).load()
    except StopIteration:
        raise ResourceNotFound('Resource "%s" not found in namespace "%s"' % (namespace, name))

def LoadClasses(namespace, name=None, condition=None, type_=object):
    """
    Load one or more classes from entry points according to some conditions

    :type namespace: str
    :type name: None or str
    :param condition: parameter given to a class' check() method
    :param type_: required type of class
    :type type_: type
    :return: List of classes
    :rtype: list
    """
    return [
        c for c in [ep.load()
            for ep in iter_entry_points(namespace, name)]
            if (c.extensionCheck(condition) if 'extensionCheck' in vars(c) else True) and issubclass(c, type_)
    ]

@memoize
def LoadClass(namespace, name=None, condition=None, type_=object):
    """
    Load a class from entry points according to some conditions

    :type namespace: str
    :type name: None or str
    :param condition: parameter given to a class' check() method
    :param type_: required type of class
    :type type_: type
    :return: a class
    :rtype: type
    :raise ResourceNotUnique:  if no class was found
    """
    result = LoadClasses(namespace, name, condition, type_)
    if len(result) > 1:
        raise ResourceNotUnique('More than one class matches in namespace "%s"' % namespace)
    if len(result) < 1:
        conditions = {}
        if name:
            conditions.update(name=name)
        if type_:
            conditions.update(type=type_)
        raise ResourceNotFound(
            'No class found in namespace "%s%s"' % (
                namespace,
                '' if not conditions else ' ({})'.format(', '.join('%s=%s' % (n, v) for n, v in list(conditions.items())))
            )
        )
    return result[0]
