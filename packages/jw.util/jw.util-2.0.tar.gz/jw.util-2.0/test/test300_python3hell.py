"""
Tests for python3hell module

Only meaningfull with tox
"""
from __future__ import unicode_literals
import sys
from jw.util.python3hell import Bytes2Str, SetDefaultEncoding, Open, Bytes, Str
from nose.tools import eq_

def test10_Bytes2Str():
    "Test Bytes2Str() function"
    eq_(Bytes2Str(b'x'), 'x')
    eq_(Bytes2Str(bytearray(b'x')), 'x')

def test20_SetDefaultEncoding():
    SetDefaultEncoding('utf-8')
    eq_(sys.getdefaultencoding(), 'utf-8')

def test30_Open():
    "Test Open() function"
    f = Open('/dev/stdout', 'a')
    f.write('')
    f.close()

def test40_Bytes():
    "Test Bytes() function"
    eq_(Bytes(u'x'), b'x')
    eq_(Bytes(42), b'42')

def test50_Str():
    "Test Str() function"
    eq_(Str(b'x'), u'x')
    eq_(Str(bytearray(b'x')), u'x')
    eq_(Str(42), u'42')
