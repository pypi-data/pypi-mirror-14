#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Implement files source that iterate over folders and return files based on depth and optional filters.

Author: Ronen Ness.
Since: 2016.
"""

from source_api import SourceAPI
import os
import re


class FolderSource(SourceAPI):
    """
    A recirsive folders source to scan.
    """

    def __init__(self, root, depth_limit=None, ret_files=True, ret_folders=False):
        """
        Init the folders source with root folder.
        :param root: root folder to scan.
        :param depth_limit: how many levels to go deep recursively.
                            None (default) = infinite depth.
                            0 = non recursive.
        :param ret_files: if true (default), will return files when iterating.
        :param ret_folders: if true, will return folders when iterating.
        """
        self.__root = root
        self.__depth_limit = depth_limit
        self.__ret_files = ret_files
        self.__ret_folders = ret_folders

    def filter_folder(self, folder):
        """
        Optional filter to apply on folders. If return False will skip this whole folder tree.
        """
        return True

    def next(self):
        """
        Return all files in folder.
        """
        # get depth of starting root directory
        base_depth = self.__root.count(os.path.sep)

        # walk files and folders
        for root, subFolders, files in os.walk(self.__root):

            # apply folder filter
            if not self.filter_folder(root):
                continue

            # make sure we don't pass depth limit
            if self.__depth_limit is not None:
                curr_depth = root.count(os.path.sep)
                if curr_depth - base_depth > self.__depth_limit:
                    continue

            # if need to return folders return it
            if self.__ret_folders:
                yield root

            # return files
            if self.__ret_files:
                for f in files:
                    yield os.path.join(root, f)

        # end iterator
        raise StopIteration


class FilteredFolderSource(FolderSource):
    """
    A recursive folders source to scan, with regex filter.
    """
    def __init__(self, root, regex_string, depth_limit=None, ret_files=True, ret_folders=False):
        """
        Init the folders source with root folder.
        :param root: root folder to scan.
        :param regex_string: regex expression as string to filter directories we scan.
        :param depth_limit: how many levels to go deep recursively.
                            None (default) = infinite depth.
                            0 = non recursive.
        :param ret_files: if true (default), will return files when iterating.
        :param ret_folders: if true, will return folders when iterating.
        """
        super(FilteredFolderSource, self).__init__(root, depth_limit, ret_files, ret_folders)
        self.__regex = re.compile(regex_string)

    def filter_folder(self, folder):
        """
        Optional filter to apply on folders. If return False will skip this whole folder tree.
        """
        return self.__regex.match(folder) is not None
