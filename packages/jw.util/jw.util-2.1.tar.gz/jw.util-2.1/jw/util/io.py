"""
Reader adapter
"""

from __future__ import absolute_import
from io import RawIOBase

class Reader(RawIOBase):
    """
    An I/O adapter reading from a resource using a callable supplied. This creates a readable stream from the output of
    repeated calls of a function. If the function requires parameters, they must be supplied with
    :py:func:`functools.partial`.
    """

    def __init__(self, function):
        """
        Create a Buffer object
        """
        self.function = function
        self.buffer = ''
        self.bufferPointer = 0

    def readable(self):
        """
        Return True for readable
        """
        return True

    def writable(self):
        """
        Return True for readable
        """
        return False

    def read(self, n=-1):
        """
        Read bytes

        :param n:
        :type n: int
        :rtype: str
        """
        # Try to read as much as needed
        while n == -1 or len(self.buffer) - self.bufferPointer < n:
            b = self.function()
            if not b:
                break
            self.buffer += b
        p = self.bufferPointer + n
        result = self.buffer[self.bufferPointer: p]
        self.bufferPointer = p
        return result

    read1 = read

    def readall(self):
        """
        Read as much as can

        :rtype: str
        """
        return self.read()

    def readinto(self, b):
        """
        Read into bytearray

        :type b: bytearray
        :rtype: int or None
        """
        r = self.read(len(b))
        b[:len(r)] = r
        return len(r) or None
