#!/usr/bin/env python

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

from setuptools import setup, find_packages

setup(
    name='jw.util',
    version='2.0',
    packages=find_packages(),
    namespace_packages=['jw'],
    install_requires=[
        'setuptools',
        'PyYAML',
        'six',
        'future',
    ],
    package_data={
        '': ['*.rst']
    },
    entry_points={
        'console_scripts': [
            'version = jw.util.version:_Main',
        ]
    },
    test_suite='nose.collector',
    tests_require=['Nose', 'mock'],
    author='Johnny Wezel',
    author_email='dev-jay@wezel.name',
    description='Version handling, YAML configuration, file renaming with various backup strategies',
    long_description=open('README.rst').read(),
    license='Apache2',
    platforms='POSIX',
    keywords='utility',
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    url='https://pypi.python.org/pypi/jw.util',
)
