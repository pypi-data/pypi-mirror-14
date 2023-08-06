#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Add a constant header to all files.

Author: Ronen Ness.
Since: 2016.
"""

from .. import files_iterator


class AddHeader(files_iterator.FilesIterator):
    """
    This iterator will add a constant header to all files, unless header already exist.
    For example, this can be used to add

    #!/usr/bin/python
    # -*- coding: utf-8 -*-

    To all python files.
    """

    def __init__(self, header, normalize_br=False):
        """
        Add header to files.
        :param header: header to add to all files.
        :param normalize_br: if True, will normalize \r\n into \n.
        """
        super(AddHeader, self).__init__()

        # normalize line breaks
        if normalize_br:
            header = header.replace("\r\n", "\n")

        # set header and if we want to normalize br
        self.__header = header
        self.__normalize_br = normalize_br

    def process_file(self, path, dryrun):
        """
        Add header to all files.
        """
        if dryrun:
            return path

        # get file's current header
        with open(path, "r") as infile:
            head = infile.read(len(self.__header))

        # normalize line breaks
        if self.__normalize_br:
            head = head.replace("\r\n", "\n")

        # already contain header? skip
        if head == self.__header:
            return path

        # add header to file
        self.push_header(path)

        # return processed file
        return path

    def push_header(self, filename):
        """
        Push the header to a given filename
        :param filename: the file path to push into.
        """
        # open file and read it all
        with open(filename, "r") as infile:
            content = infile.read()

        # push header
        content = self.__header + content

        # re-write file with the header
        with open(filename, "w") as outfile:
            outfile.write(content)
