#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Do "grep" on all files.
Use this as an iterator only, eg:

for line in grep.next():
    print line

Author: Ronen Ness.
Since: 2016.
"""

from .. import files_iterator
import re
import sys


class Grep(files_iterator.FilesIterator):
    """
    Iterate over files and return lines that match the grep condition.
    Return a list of lists: for every file return the list of occurances found in it.
    """
    def __init__(self, expression):
        """
        Init the grep iterator.

        :param expression: the grep expression to look for.
        """
        super(Grep, self).__init__()
        self.__exp = expression

    def set_grep(self, expression):
        """
        Change / set the grep expression.
        """
        self.__exp = expression

    def process_file(self, path, dryrun):
        """
        Print files path.
        """
        # if dryrun just return files
        if dryrun:
            return path

        # scan file and match lines
        ret = []
        with open(path, "r") as infile:
            for line in infile:
                if re.search(self.__exp, line):
                    ret.append(line)

        # if found matches return list of lines, else return None
        return ret if len(ret) > 0 else None
