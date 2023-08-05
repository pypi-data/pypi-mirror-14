# Copyright 2014 Johnny Wezel
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
This module provides a class for splitting strings in a shell-like manner.
"""

WHITE_SPACE = ' \t\r\n\f'
NEXT_STATE = {
    ' ': 0,
    '\t': 0,
    '\r': 0,
    '\n': 0,
    '\f': 0,
    '"': 2,
    "'": 3
}

class Splitter(object):

    def __init__(self, s):

        """
        Create Splitter object

        :param s: string to split
        :type s: str
        """
        self.s = s
        self.p = 0
        self.args = []
        self.states = self.state0, self.state1, self.state2, self.state3
        self.state = self.states[0]

    def split(self):
        """
        Split

        :return: list of parts
        :rtype: list
        """
        while True:
            st = self.state()
            if st == 'end':
                break
            if st is not None:
                self.state = self.states[st]
        return self.args

    @property
    def c(self):
        try:
            c = self.s[self.p]
        except IndexError:
            return None
        self.p += 1
        return c

    @property
    def c0(self):
        try:
            c = self.s[self.p]
        except IndexError:
            return None
        return c

    def state0(self):
        c = self.c0
        if not c:
            return 'end'
        if c not in WHITE_SPACE:
            self.args.append('')
            return 1
        self.p += 1

    def state1(self):
        c = self.c
        if not c:
            return 0
        try:
            st = NEXT_STATE[c]
            return st
        except KeyError:
            self.args[-1] += c

    def state2(self):
        c = self.c
        if not c:
            raise ValueError('Unclosed double quote')
        if c == '"':
            return 0
        self.args[-1] += c

    def state3(self):
        c = self.c
        if not c:
            raise ValueError('Unclosed single quote')
        if c == "'":
            return 0
        self.args[-1] += c
