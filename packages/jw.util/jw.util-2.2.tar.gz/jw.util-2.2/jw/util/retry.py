"""
Retry function
"""
from __future__ import absolute_import, print_function
from time import time, sleep
import types

def retry(
    function,
    *args,
    **kw
):
    """
    Retry a function call

    :param function: function to call
    :param float for_: time limit (sec)
    :param int times_: tries limit
    :param function logSuccess_: callable to call on success
    :param function logFailure_: callable to call on failure
    :param float initialWait_: initial wait after error
    :param waitExpand_: multiplier for successive wait intervals
    :param failure_: Exception or callable or object to be raised/returned after retry limit reached
    :param tuple args: ar
    :param dict kw:
    :return: function result

    Tries a function until either it succeeds (does not raise), time (`for_`) runs out or number of tries (`times_`)
    is exceeded. If neither criteria is supplied, the function is tried for ever. If exception is provided, only this
    exception (or exceptions if it's iterable) are handled. All unmentioned exceptions occurring will be re-thrown.
    """
    # Get own arguments from keywords
    for_=kw.pop('for_', None)
    times_=kw.pop('times_', None)
    logSuccess_=kw.pop('logSuccess_', None)
    logFailure_=kw.pop('logFailure_', None)
    exception_=kw.pop('exception_', None)
    initialWait_=kw.pop('initialWait_', 1)
    waitExpand_=kw.pop('waitExpand_', 2)
    failure_=kw.pop('failure_', None)
    # Initialize
    tries = 0
    begun = time()
    wait = initialWait_
    result = None
    # Try
    while True:
        if times_ and tries >= times_:
            break
        if for_ and time() >= begun + for_:
            break
        try:
            result = function(*args, **kw)
            if logSuccess_:
                logSuccess_()
            return result
        except Exception as e:
            if exception_:
                if hasattr(exception_, '__iter__'):
                    if e.__class__ not in exception_:
                        raise
                else:
                    if e.__class__ is not exception_:
                        raise
            if logFailure_:
                logFailure_(e)
            sleep(wait)
            wait *= waitExpand_
        tries += 1
    # No more tries
    if failure_:
        if callable(failure_):
            failure_ = failure_()
        if isinstance(failure_, Exception):
            raise failure_
        result = failure_
    return result
