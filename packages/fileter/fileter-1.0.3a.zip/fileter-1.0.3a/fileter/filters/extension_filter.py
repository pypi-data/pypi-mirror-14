#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Implement a simple filter by file extension.

Author: Ronen Ness.
Since: 2016.
"""
from filter_api import FilterAPI


class FilterExtension(FilterAPI):
    """
    A simple filter by a file extensions.
    """
    def __init__(self, extensions):
        """
        Create the extensions filter.
        :param extensions: a single extension or a list of extensions to accept.
                            Note: without the dot, for example: ["py", "js", "cpp", ...]
        """
        self.__extensions = extensions if isinstance(extensions, (list, tuple)) else [extensions]

    def match(self, filepath):
        """
        The function to check file.
        Should return True if match, False otherwise.
        """
        # no extension?
        if filepath.find(".") == -1:
            return False

        # match extension
        return filepath.lower().split(".")[-1] in self.__extensions
