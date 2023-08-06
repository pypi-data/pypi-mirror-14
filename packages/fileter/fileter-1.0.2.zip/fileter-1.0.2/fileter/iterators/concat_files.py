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

    def on_start(self):
        """
        Open the output file.
        """
        self._output = open(self._output_path, "wb")

    def on_end(self):
        """
        Close the output file.
        """
        self._output.close()

    def process_file(self, path):
        """
        Concat files and return filename.
        """
        # special case - skip output file so we won't include it in result
        if path == self._output_path:
            return None

        # add file
        with open(path, "rb") as infile:
            data = infile.read()
            self._output.write(data)

        # return processed file
        return path
