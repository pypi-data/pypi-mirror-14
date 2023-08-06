#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Implement a simple filter by regex expression.

Author: Ronen Ness.
Since: 2016.
"""
from filter_api import FilterAPI
import re


class FilterRegex(FilterAPI):
    """
    A simple filter by a regex expression.
    """
    def __init__(self, regex_string):
        """
        Create the regex filter.
        :param regex_string: regex expression string to filter by.
        """
        self.__regex = re.compile(regex_string)

    def match(self, filepath):
        """
        The function to check file.
        Should return True if match, False otherwise.
        """
        return self.__regex.match(filepath) is not None
