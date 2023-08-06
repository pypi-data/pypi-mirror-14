#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Implement files source that iterate over folders and return files using fnmatch patterns (linux style file patterns).

Author: Ronen Ness.
Since: 2016.
"""
from source_api import SourceAPI
import fnmatch
import os


class PatternSource(SourceAPI):
    """
    A recursive folders scanner with pattern.
    """
    def __init__(self, pattern, root='.', depth_limit=None, ret_files=True, ret_folders=False):
        """
        Init the folders source with root folder.
        :param pattern: fnmatch pattern(s) to match.
                        can be a single string or a list of strings.
        :param root: root folder to scan. default to '.'.
        :param depth_limit: how many levels to go deep recursively.
                            None (default) = infinite depth.
                            0 = non recursive.
        :param ret_files: if true (default), will return files when iterating.
        :param ret_folders: if true, will return folders when iterating.
        """
        self.__pattern = pattern if isinstance(pattern, (list, tuple)) else [pattern]
        self.__root = root
        self.__depth_limit = depth_limit
        self.__ret_files = ret_files
        self.__ret_folders = ret_folders

    def next(self):
        """
        Return all files in folder.
        """
        # get depth of starting root directory
        base_depth = self.__root.count(os.path.sep)

        # walk files and folders
        for root, subFolders, files in os.walk(self.__root):

            # make sure we don't pass depth limit
            if self.__depth_limit is not None:
                curr_depth = root.count(os.path.sep)
                if curr_depth - base_depth > self.__depth_limit:
                    continue

            # if required to return folders and folder match patterns, return folder
            if self.__ret_folders and self.match_pattern(root):
                yield root

            # iterate files
            for f in files:

                # get current file path
                curr_file = os.path.join(root, f)

                # if match return file
                if self.match_pattern(curr_file):
                    yield curr_file

        # end iterator
        raise StopIteration

    def match_pattern(self, path):
        """
        Return if given path match the pattern(s).

        :param path: path to check.
        :return: True if match, False otherwise.
        """
        for pattern in self.__pattern:
            if len(fnmatch.filter([path], pattern)) > 0:
                return True
        return False
