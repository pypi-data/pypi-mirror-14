#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Iterate files and concat them into one big file.

Author: Ronen Ness.
Since: 2016.
"""

from .. import files_iterator


class ConcatFiles(files_iterator.FilesIterator):
    """
    This files iterator concat all scanned files.
    """

    def __init__(self, outfile):
        """
        concat all source files into one output file.
        :param outfile: output file path.
        """
        super(ConcatFiles, self).__init__()
        self._output_path = outfile
        self._output_file = None

    def on_start(self, dryrun):
        """
        Open the output file.
        """
        if not dryrun:
            self._output_file = open(self._output_path, "wb")

    def on_end(self, dryrun):
        """
        Close the output file.
        """
        if not dryrun:
            self._output_file.close()

    def process_file(self, path, dryrun):
        """
        Concat files and return filename.
        """
        # special case - skip output file so we won't include it in result
        if path == self._output_path:
            return None

        # if dryrun skip and return file
        if dryrun:
            return path

        # concat file with output file
        with open(path, "rb") as infile:
            data = infile.read()
            self._output_file.write(data)

        # return processed file path
        return path
