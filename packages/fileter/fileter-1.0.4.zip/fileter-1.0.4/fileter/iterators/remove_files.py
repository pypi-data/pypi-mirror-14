#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Iterate files and remove them.

Author: Ronen Ness.
Since: 2016.
"""

from .. import files_iterator
import os


class RemoveFiles(files_iterator.FilesIterator):
    """
    This iterator will remove all files.
    """

    def __init__(self, force=False):
        """
        concat all source files into one output file.
        :param force: if true, will just remove all files. Else, will ask for every file before.
        """
        super(RemoveFiles, self).__init__()
        self.__force = force

    def process_file(self, path, dryrun):
        """
        Remove files and return filename.
        """
        # if dryrun just return file path
        if dryrun:
            return path

        # remove and return file
        if self.__force or raw_input("Remove file '%s'? [y/N]" % path).lower() == "y":
            os.remove(path)
            return path

