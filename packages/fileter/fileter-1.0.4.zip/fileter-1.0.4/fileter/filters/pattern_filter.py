#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Implement a simple filter by file pattern.

Author: Ronen Ness.
Since: 2016.
"""
from filter_api import FilterAPI
import fnmatch


class FilterPattern(FilterAPI):
    """
    A simple filter by linux-style file patterns.
    """
    def __init__(self, pattern):
        """
        Create the extensions filter.
        :param pattern: a single pattern or a list of patterns to accept.
        """
        self.__pattern = pattern if isinstance(pattern, (list, tuple)) else [pattern]

    def match(self, filepath):
        """
        The function to check file.
        Should return True if match, False otherwise.
        """
        for pattern in self.__pattern:
            if len(fnmatch.filter([filepath], pattern)) > 0:
                return True
        return False
