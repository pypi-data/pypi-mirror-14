"""
Test retry module
"""
from __future__ import print_function
from time import sleep
from nose.tools import eq_, raises
from jw.util.retry import retry

called = 0

def func(question):
    global called
    called += 1
    if called < 3:
        raise RuntimeError('Test')
    return 42

def func2(question):
    global called
    sleep(.3)
    called += 1
    if called < 3:
        raise RuntimeError('Test')
    return 42

def test10_retryTimesSuccess():
    """Test retry(..., times_=x)"""
    global called
    called = 0
    eq_(retry(func, 'why', times_=3, initialWait_=0), 42)
    eq_(called, 3)

@raises(RuntimeError)
def test20_retryTimesFailure():
    """Test retry(..., times_=x) exceeded"""
    global called
    called = 0
    retry(func, 'why', times_=2, initialWait_=0, failure_=RuntimeError('Nope'))
    eq_(called, 2)

def test10_retryUntilSuccess():
    """Test retry(..., until_=x)"""
    global called
    called = 0
    eq_(retry(func2, 'why', for_=1., initialWait_=0), 42)
    eq_(called, 3)

@raises(RuntimeError)
def test20_retryUntilFailure():
    """Test retry(..., until_=x)"""
    global called
    called = 0
    retry(func2, 'why', for_=.5, initialWait_=0, failure_=RuntimeError('Nope')),
    eq_(called, 2)
