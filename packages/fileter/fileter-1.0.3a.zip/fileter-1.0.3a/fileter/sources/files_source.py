#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Implement a source that is just a single file or a constant list of filenames.

Author: Ronen Ness.
Since: 2016.
"""
from source_api import SourceAPI


class FileSource(SourceAPI):
    """
    A single-file or a list of files source.
    """

    def __init__(self, filepath):
        """
        Init the source file.
        :param filepath: path of the file. Can also be a list of files.
        """
        self.__path = filepath if isinstance(filepath, (list, tuple)) else [filepath]

    def __iter__(self):
        """
        Return the file source(s) as list.
        """
        return iter(self.__path)

    def next(self):
        """
        Return the file.
        """
        for i in self.__path:
            yield i
        raise StopIteration

    def get_files(self):
        """
        Return the file source.
        """
        return self.__path
