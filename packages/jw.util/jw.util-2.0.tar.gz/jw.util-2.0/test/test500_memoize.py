"""
Test memoize decorators
"""
from __future__ import print_function
from nose.tools import eq_
import time
from jw.util.memoize import memoize, memoizeFor, memoizeUpto

addCalled = 0
subCalled = 0
mulCalled = 0

@memoize
def add(a, b):
    global addCalled
    addCalled += 1
    return a + b

@memoizeFor(1)
def sub(a, b):
    global subCalled
    subCalled += 1
    return a - b

@memoizeUpto(2)
def mul(a, b):
    global mulCalled
    mulCalled += 1
    return a * b

def test10_simpleMemoize():
    eq_(add(1, 2), add(1, 2))
    eq_(addCalled, 1)
    eq_(add(3, 2), add(3, 2))
    eq_(addCalled, 2)
    eq_(len(add.cache), 2)

def test20_memoizeFor():
    eq_(sub(3, 2), sub(3, 2))
    eq_(subCalled, 1)
    r1 = sub(4, 3)
    eq_(subCalled, 2)
    time.sleep(2)
    r2 = sub(4, 3)
    eq_(subCalled, 3)
    eq_(r1, r2)

def test30_memoizeUpto():
    eq_(mul(2, 3), mul(2, 3))
    eq_(mulCalled, 1)
    eq_(mul(4, 3), mul(4, 3))
    eq_(mulCalled, 2)
    mul(2, 3)
    eq_(mulCalled, 2)
    mul(5, 3)
    eq_(mulCalled, 3)
    mul(2, 3)
    eq_(mulCalled, 4)
    mul(5, 3)
    eq_(mulCalled, 4)
