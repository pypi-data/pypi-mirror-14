#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Filters used to determine which files to process and which files we want to skip.
For example, you can filter files by extension, etc.

This file define the filter API class.

Note: filters should NOT do any action that modify content, eg anything that is not read-only stuff.
This is because filters are applied even when calling dry-runs. So are expected not to make any changes.

Author: Ronen Ness.
Since 2016.
"""


class FilterAPI(object):
    """
    API for a filter to determine if we want to process a given file or skip it.
    Inherit from this class and implement "match()" function to create filter.
    """

    def match(self, filepath):
        """
        The function to check file.
        Should return True if match, False otherwise.
        """
        raise NotImplementedError()
