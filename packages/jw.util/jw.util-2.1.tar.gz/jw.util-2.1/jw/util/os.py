"""
Helpers for stuff related to the operating system
"""
from __future__ import print_function
from __future__ import absolute_import

import pwd
import os

_Passwd = pwd.getpwuid(os.geteuid())
# Default environment
_DEFAULT_ENVIRONMENT = {
    'LOGNAME': _Passwd.pw_name,
    'USER': _Passwd.pw_name,
    'HOME': _Passwd.pw_dir,
    'LANG': 'en_US.UTF-8',
    'PATH': '{HOME}/.local/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin'.format(
        HOME=_Passwd.pw_dir
    ),
}

def SetMinimalEnvironment(override=None, **additionalSettings):
    """
    Set up a minimal set of environment variables

    :param override: None (default) or iterable of variable names to set forcibly, whether they are present or not
    :param additionalSettings: keyword arguments setting additional variables

    See modul's `_DEFAULT_ENVIRONMENT` variable for the default set of names
    """
    if override is None:
        override = ()
    else:
        assert hasattr(override, '__iter__'), "Parameter 'override' must be None or iterable, got %s" % repr(override)
    variables = _DEFAULT_ENVIRONMENT.copy()
    variables.update(additionalSettings)
    for k, v in list(variables.items()):
        if k not in os.environ or k in override:
            os.putenv(k, v)
            os.environ[k] = v
