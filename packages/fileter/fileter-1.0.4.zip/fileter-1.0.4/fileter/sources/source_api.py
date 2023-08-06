#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
A source object is a source of files to iterate / process.
It can be something simple like a single file, a list of files, a recursively scanned directory, etc.
Or more complicated stuff like a source that generate new file names based on some algorithm etc.

This package comes with all the basic sources you need for individual files and for scanning folders.
To create a more sophisticated source types inherit from SourceAPI and implement the required methods.

Author: Ronen Ness.
Since 2016.
"""


class SourceAPI(object):
    """
    API for a source of files.
    Inherit from this class and implement the required functions to create a customized source type.
    """

    def __iter__(self):
        """
        Implement the iter function so we'll be able to iterate over this source.
        See python iteratable docs for more info.
        """
        return self.next()

    def next(self):
        """
        This is the main function you need to implement, which iterate over your source files.

        See python iteratables protocol for more info, but in short you just need to do the following:
        1. if you got next value to return, return it using yield.
        2. when you have no more values, raise StopIteration exception.
        """
        raise NotImplementedError()

    def get_all(self):
        """
        return all files in this source as list.
        """
        return [x for x in iter(self)]

