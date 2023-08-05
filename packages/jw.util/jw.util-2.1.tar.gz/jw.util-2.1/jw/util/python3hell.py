# Copyright 2016 Johnny Wezel
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

"""
Tools for handling Python3 hell
"""

from __future__ import print_function, unicode_literals
from builtins import bytes
from builtins import str

import errno
from six import PY2

if PY2:

    def Bytes2Str(b):
        """
        Convert to str/unicode if it's a byte or bytearray type

        :param b: str or bytes
        :return: string
        :rtype: str

        Convert `line` to str by decode() if it's a byte type. It's a good idea to do the setdefaultencoding() hack.
        Does not check for other types.
        """
        return b.decode('utf-8', errors='replace') if isinstance(b, (bytes, bytearray)) else b

    def Bytes(s):
        """
        Convert anything to bytes

        :param s:
        :rtype: bytes
        """
        return bytes(s) if isinstance(s, (bytes, bytearray)) else str(s).encode('utf-8', errors='replace')

    def Str(o):
        """
        Convert object to str/unicode

        :param o:
        :rtype: unicode
        """
        return o if isinstance(o, str) else str(o)

    def SetDefaultEncoding(encoding='utf-8'):
        """
        Do the setdefaultencoding hack

        :param encoding: encoding (default: 'utf-8')
        :type encoding: str
        """
        import sys
        reload(sys)
        sys.setdefaultencoding(encoding)

    def Open(*args, **kwargs):
        """
        Open a file

        :param args:
        :param kwargs:
        """
        return open(*args, **kwargs)

else:  # Python >= 3

    def Bytes2Str(o):
        """
        Convert to str if it's a byte or bytearray type

        :param o: str or bytes
        :return: string
        :rtype: str

        Convert `line` to str by decode() if it's a byte type. It's a good idea to do the setdefaultencoding() hack.
        Does not check for other types.
        """
        return o.decode('utf-8', errors='replace') if isinstance(o, (bytes, bytearray)) else o

    def Bytes(s):
        """
        Convert anything to bytes

        :param s:
        :rtype: bytes
        """
        return s if isinstance(s, (bytearray, bytes)) else str(s).encode('utf-8', errors='replace')

    def Str(o):
        """
        Convert object to str

        :param o:
        :rtype: str
        """
        return (
            o
                if isinstance(o, str)
                else o.decode('utf-8', errors='replace')
                    if isinstance(o, (bytes, bytearray))
                    else str(o)
        )

    def SetDefaultEncoding(encoding='utf-8'):
        """
        Do the setdefaultencoding hack

        :param encoding: encoding (default: 'utf-8')
        :type encoding: str
        """

    def Open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        """
        Open a file

        :param file:
        :param mode:
        :param buffering:
        :param encoding:
        :param errors:
        :param newline:
        :param closefd:
        :param opener:
        :return: :rtype: :raise:
        """
        try:
            return open(file, mode, buffering, encoding, errors, newline, closefd, opener)
        except OSError as e:
            # Work around Python3 hell
            if e.errno == errno.ESPIPE and mode == 'a':
                return open(file, 'w', buffering, encoding, errors, newline, closefd, opener)
            raise
