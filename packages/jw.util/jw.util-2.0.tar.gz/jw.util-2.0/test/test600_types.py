"""
Test types module
"""
from nose.tools import eq_
from jw.util.types import Args2Str

def test10_Args2Str():
    """Test Arg22Str"""
    eq_(Args2Str(*(42, 'world')), "42, 'world'")
    eq_(Args2Str(*(42, 'world'), **{'world': 42}), "42, 'world', world=42")
