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
This module provides the :py:class:`Backup` class.


The :py:class:`Backup` class can be used as follows:

    >>> from jw.util.file import Backup
    >>> open('myfile','w')
    <open file 'myfile', mode 'w' at ...>
    >>> backup = Backup('myfile')
    >>> backup()
    >>> import glob
    >>> glob.glob('myfile*')
    ['myfile~']
"""
from __future__ import absolute_import
from builtins import object
import shutil

import os
from six import text_type, binary_type

class Backup(object):
    """
    File backup

    Organizes file 'backup' by renaming it and it's old backups recursively.

    :param filename: path to file to handle
    :type filename: str
    :param mode: backup mode (see table)
    :type mode: various

    Renames a file according to mode. Previous renamed versions are recursively renamed as well. The filename
    suffixes and the number of generations are set as follows:

    +---------------+-----------+---------------+
    | mode          | suffix    | generations   |
    +===============+===========+===============+
    | False         |           | 0             |
    +---------------+-----------+---------------+
    | True          | ~         | 1             |
    +---------------+-----------+---------------+
    | str           | str       | 1             |
    +---------------+-----------+---------------+
    | int           | .i        | n             |
    +---------------+-----------+---------------+
    | (str, int)    | str       | n             |
    +---------------+-----------+---------------+

    A generations specifier of -1 means unlimited. Integer-based generations are generated as a dot plus the integer (eg.
    filename.1, filename.2 etc). String-based generations are generated as multiple concatenations of the string (eg.
    filename~, filename~~ etc).

    Note that zero generations means *no* backup is made, but the original file "moved out of the way", resulting in the file
    being deleted.
    """

    def __init__(self, filename, mode=True):
        """
        Create Backup object
        """
        self.filename = filename
        # noinspection PySimplifyBooleanCheck
        if mode in (False, None):
            self.generations = 0
            self.string = '?'
            self.suffix = self._stringSuffix
        elif mode is True:
            self.generations = 1
            self.string = '~'
            self.suffix = self._stringSuffix
        elif isinstance(mode, int):
            self.generations = mode
            self.suffix = self._intSuffix
        elif isinstance(mode, (binary_type, text_type)):
            self.generations = 1
            self.suffix = self._stringSuffix
            self.string = mode
        elif isinstance(mode, (tuple, list)) and isinstance(mode[0], (binary_type, text_type)) and isinstance(mode[1], int):
            self.generations = mode[1]
            self.suffix = self._stringSuffix
            self.string = mode[0]

    def _stringSuffix(self, level):
        return level * self.string

    def _intSuffix(self, level):
        return '.%d' % level if level else ''

    def __call__(self):
        """
        Perform backup

        Runs the operation
        """
        self._run(0)

    def _run(self, level):
        """
        Backup level

        :param level:
        :type level: int
        """
        if self.generations < 0 or level < self.generations:
            oldName = self.filename + self.suffix(level)
            if os.path.exists(oldName):
                newName = self.filename + self.suffix(level + 1)
                if os.path.exists(newName):
                    try:
                        self._run(level + 1)
                    except Exception as e:
                        raise RuntimeError('Could not move {} out of the way. Reason:\n{}'.format(newName, e))
                try:
                    os.rename(oldName, newName)
                except Exception as e:
                    raise RuntimeError('Could not rename {} to {} because {}'.format(oldName, newName, e))
        else:
            name = self.filename + self.suffix(level)
            if os.path.exists(name):
                # Ran out of generations. Remove this level
                try:
                    if os.path.isdir(name):
                        op = 'remove directory'
                        shutil.rmtree(name)
                    else:
                        op = 'remove file'
                        os.remove(name)
                except Exception as e:
                    raise RuntimeError('Could not {} because {}'.format(op, e))
