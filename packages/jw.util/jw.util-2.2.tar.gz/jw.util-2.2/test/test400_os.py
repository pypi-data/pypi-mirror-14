"""
Test os module
"""
from nose.tools import eq_
import os

from jw.util.os import SetMinimalEnvironment

def test10_SetMinimalEnvironment():
    'Test SetMinimalEnvironment()'
    del os.environ['HOME']
    SetMinimalEnvironment()
    assert 'HOME' in os.environ

def test20_SetMinimalEnvironment():
    'Test SetMinimalEnvironment(override=)'
    UNKNOWN = '*unknown*'
    os.environ['HOME'] = UNKNOWN
    SetMinimalEnvironment(override=('HOME',))
    assert os.environ['HOME'] != UNKNOWN

def test30_SetMinimalEnvironment():
    'Test SetMinimalEnvironment() existent non-override'
    PREVIOUS = '*previous*'
    os.environ['HOME'] = PREVIOUS
    SetMinimalEnvironment(HOME='*new*')
    eq_(os.environ['HOME'], PREVIOUS)

def test40_SetMinimalEnvironment():
    'Test SetMinimalEnvironment() existent override'
    PREVIOUS = '*previous*'
    NEW = '*new*'
    os.environ['HOME'] = PREVIOUS
    SetMinimalEnvironment(override=('HOME',), HOME=NEW)
    eq_(os.environ['HOME'], NEW)
