jw.util
=======

This package contains various utility modules:

version
    a module for version management: incrementing/decrementing specific levels of a version, parsing and a utility to
    update versions in a file.

file
    a module to do stuff on whole files. At the moment, the only thing in it is a class for backing up a file by
    renaming it with various strategies for renaming previous "backups": adding a simple suffix or adding a numbered
    suffix

configuration
    a module for handling configurations from a YAML source and a class for simplifying access to a configuration tree

python3hell
    a module with helpers to mitigate Python3 hell
