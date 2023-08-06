#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Simple iterator that print all files.

Author: Ronen Ness.
Since: 2016.
"""

from .. import files_iterator


class PrintFiles(files_iterator.FilesIterator):
    """
    Iterate over files and print their names.
    """

    def process_file(self, path, dryrun):
        """
        Print files path.
        """
        if not dryrun:
            print path
        return path
