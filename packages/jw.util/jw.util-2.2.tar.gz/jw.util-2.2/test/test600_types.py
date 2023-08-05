"""
Test types module
"""
from nose.tools import eq_
from jw.util.types import Args2Str, Abbr


def test10_Args2Str():
    """Test Arg22Str"""
    eq_(Args2Str(*(42, 'world')), "42, 'world'")
    eq_(Args2Str(*(42, 'world'), **{'world': 42}), "42, 'world', world=42")

def test20_Abbr():
    """Test Abbr"""
    eq_(Abbr('jump', 10), 'jump')
    eq_(Abbr('jump'), 'jump')
    eq_(Abbr('jump', 3), 'jum...')
