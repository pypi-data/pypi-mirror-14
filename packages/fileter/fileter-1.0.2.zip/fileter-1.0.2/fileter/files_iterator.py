#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Base class to iterate file sources and run a function on all files.
The iteration will iterate over files paths, its up to you to open files etc.

Author: Ronen Ness.
Since: 2016
"""
from sources import *
from filters import *


class FilesIterator(object):
    """
    Base class to iterate over file sources and perform pre-defined actions on them.

    This class can be used in two ways:
    1. as an iterator, if you want to iterate files and use them externally.
    2. as an object that have pre-defined processing function and can iterate and process files internally.

    For example, we can implement an iterator that iterate over files and add a comment to every first line.
    Weather you use this as an iterator or as an object, all file paths will be processed via the process_file() function.
    """

    def __init__(self):
        """
        Init the iterator.
        """
        self.__sources = []
        self.__filters = []

    def add_source(self, source):
        """
        Add a source to this iterator.

        :param source: files source, must be an object inheriting from sources.SourceAPI.
        """
        self.__sources.append(source)
        return self

    def add_file(self, filepath):
        """
        Add a single file source from path (string).

        :param filepath: file path as string. can also be a list of files.
        """
        self.add_source(FileSource(filepath))
        return self

    def add_folder(self, path, depth=None):
        """
        Add a folder source to scan recursively from path (string).

        :param path: folder path.
        :param depth: if provided will be depth limit. 0 = first level only.
        """
        self.add_source(FolderSource(path, depth))
        return self

    def add_filtered_folder(self, path, regex, depth=None):
        """
        Add a folder source to scan recursively, with a regex filter on directories.

        :param regex: regex string to filter folders by.
        :param depth: if provided will be depth limit. 0 = first level only.
        """
        self.add_source(FilteredFolderSource(path, regex, depth))
        return self

    def add_filter(self, files_filter):
        """
        Add a files filter to this iterator.

        :param files_filter: filter to apply, must be an object inheriting from filters.FilterAPI.
        """
        self.__filters.append(files_filter)
        return self

    def add_filter_by_regex(self, regex_expression):
        """
        Add a files filter by regex to this iterator.

        :param regex_expression: regex string to apply.
        """
        self.add_filter(FilterRegex(regex_expression))
        return self

    def add_filter_by_extension(self, extensions):
        """
        Add a files filter by extensions to this iterator.

        :param extensions: single extension or list of extensions to filter by.
                            for example: ["py", "js", "cpp", ...]
        """
        self.add_filter(FilterExtension(extensions))
        return self

    def __iter__(self):
        """
        Return self as iterator.
        """
        return self.next()

    def get_files(self):
        """
        return all files in this iterator as list.
        """
        return [x for x in iter(self)]

    def process_all(self):
        """
        Iterate internally over all files and call process_file().
        Use this function if you want to use this iterator with pre-defined processing function, and not
        for external iteration.
        """
        for _ in self.next():
            pass

    def dry_run(self):
        """
        Iterate over all files and just print them.
        This will not call "process_file()", this will only fetch files from all sources
        and apply filters on them.
        """
        for f in self.next(dryrun=True):
            print f

    def next(self, dryrun=False):
        """
        Iterate over files in all sources.
        Use this if you want to iterate files externally.

        :param dryrun: if true, will only return all filenames instead of processing them, eg will not
                        call "process_file" at all, and just show all the files it will scan.
        """

        # call the start hook
        self.on_start()

        # iterate over sources
        for src in self.__sources:

            # iterate over files
            for filename in src.next():

                # make sure file pass filters
                if not self.match_filters(filename):
                    continue

                # if we are in dryrun mode, stop and return here
                if dryrun:
                    yield filename
                    continue

                # process file
                curr = self.process_file(filename)

                # if after process we still want to return file for external iteration, return it
                if curr is not None:
                    yield curr

        # call the end iteration hook and raise stop iteration exception
        self.on_end()
        raise StopIteration

    def on_start(self):
        """
        A hook you can implement to be called when an iteration starts.
        For example, you can use this to open output file, log, etc.
        """
        pass

    def on_end(self):
        """
        A hook you can implement to be called when an iteration ends.
        For example, you can use this to close output file, log, etc.
        """
        pass

    def match_filters(self, path):
        """
        Get filename and return True if file pass all filters and should be processed.

        :param path: path to check.
        :return: True if pass filters, false otherwise.
        """
        for filter in self.__filters:
            if not filter.match(path):
                return False
        return True

    def process_file(self, path):
        """
        This function is called for every file processed.
        When using this class as an iterator, this function can return None to skip files, or
        process their names before returned.

        :param path: current file path.
        :return: should return filename, or None if you want to omit this file from the iteration loop.
        """
        return path
