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
import os


class FilesIterator(object):
    """
    Base class to iterate over file sources and perform pre-defined actions on them.

    This class can be used in two ways:
    1. as an iterator, if you want to iterate files and use them externally.
    2. as an object that have pre-defined processing function and can iterate and process files internally.

    For example, we can implement an iterator that iterate over files and add a comment to every first line.
    Weather you use this as an iterator or as an object, all file paths will be processed via the process_file() function.
    """

    # type of filters we can add to the iterator, and how to use them
    class FilterType:

        # All required filters must match in order for a file to be processed.
        # for example, if you have 2 required filters and file only match 1, it will be ignored.
        Required = 0

        # If file matches at least one Include filter, it will be processed immediately, even if doesn't
        # match all required filters. Note: this filter type collide with Exclude; first filter to match
        # will determine if the file will be processed or not. Order of filters is meaningful.
        Include = 1

        # If file matches at least one Exclude filter, it will be ignored immediately, even if it
        # match all required filters. Note: this filter type collide with Include; first filter to match
        # will determine if the file will be processed or not. Order of filters is meaningful.
        Exclude = 2

    # define the default filter type
    DefaultFilterType = FilterType.Required

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

    def add_pattern(self, pattern, root=".", depth=None):
        """
        Add a recursive folder scan using a linux-style patterns.

        :param pattern: pattern or list of patterns to match.
        :param root: root to start from (default to '.')
        :param depth: if provided will be depth limit. 0 = first level only.
        """
        self.add_source(PatternSource(pattern, root, depth))
        return self

    def add_filtered_folder(self, path, regex, depth=None):
        """
        Add a folder source to scan recursively, with a regex filter on directories.

        :param regex: regex string to filter folders by.
        :param depth: if provided will be depth limit. 0 = first level only.
        """
        self.add_source(FilteredFolderSource(path, regex, depth))
        return self

    def add_filter(self, files_filter, filter_type=DefaultFilterType):
        """
        Add a files filter to this iterator.
        For a file to be processed, it must match ALL filters, eg they are added with ADD, not OR.

        :param files_filter: filter to apply, must be an object inheriting from filters.FilterAPI.
        :param filter_type: filter behavior, see FilterType for details.
        """
        self.__filters.append((files_filter, filter_type))
        return self

    def add_filter_by_pattern(self, pattern, filter_type=DefaultFilterType):
        """
        Add a files filter by linux-style pattern to this iterator.

        :param pattern: linux-style files pattern (or list of patterns)
        """
        self.add_filter(FilterPattern(pattern), filter_type)
        return self

    def add_filter_by_regex(self, regex_expression, filter_type=DefaultFilterType):
        """
        Add a files filter by regex to this iterator.

        :param regex_expression: regex string to apply.
        """
        self.add_filter(FilterRegex(regex_expression), filter_type)
        return self

    def add_filter_by_extension(self, extensions, filter_type=DefaultFilterType):
        """
        Add a files filter by extensions to this iterator.

        :param extensions: single extension or list of extensions to filter by.
                            for example: ["py", "js", "cpp", ...]
        """
        self.add_filter(FilterExtension(extensions), filter_type)
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
        self.on_start(dryrun)

        # store current dir
        curr_dir = ""

        # iterate over sources
        for src in self.__sources:

            # call the start_source hook
            self.on_start_source(src, dryrun)

            # iterate over files
            for filename in src.next():

                # make sure file pass filters
                if not self.match_filters(filename):
                    continue

                # get curr dir to call the directory-enter hook
                new_curr_dir = os.path.dirname(filename)
                if new_curr_dir != curr_dir:
                    self.on_enter_dir(new_curr_dir, dryrun)
                    curr_dir = new_curr_dir

                # process file
                curr = self.process_file(filename, dryrun)

                # if after process we still want to return file for external iteration, return it
                if curr is not None:
                    yield curr

            # call the end-source hook
            self.on_end_source(src, dryrun)

        # call the end iteration hook and raise stop iteration exception
        self.on_end(dryrun)
        raise StopIteration

    def on_enter_dir(self, directory, dryrun):
        """
        A hook you can implement to be called when iteration changes directory (called when entered / exit
        directories while scanning)

        :param directory: the directory we are now in.
        :param dryrun: indicate if we are currently in dry-run mode and should not change files.
        """
        pass

    def on_start_source(self, source, dryrun):
        """
        A hook you can implement to be called when a new source is starting to be processed.
        :param source: the source we started processing.

        :param dryrun: indicate if we are currently in dry-run mode and should not change files.
        """
        pass

    def on_end_source(self, source, dryrun):
        """
        A hook you can implement to be called when we finish iterating a source.
        :param source: the source we finished processing.

        :param dryrun: indicate if we are currently in dry-run mode and should not change files.
        """
        pass

    def on_start(self, dryrun):
        """
        A hook you can implement to be called when an iteration starts.
        For example, you can use this to open output file, log, etc.

        :param dryrun: indicate if we are currently in dry-run mode and should not change files.
        """
        pass

    def on_end(self, dryrun):
        """
        A hook you can implement to be called when an iteration ends.
        For example, you can use this to close output file, log, etc.

        :param dryrun: indicate if we are currently in dry-run mode and should not change files.
        """
        pass

    def match_filters(self, path):
        """
        Get filename and return True if file pass all filters and should be processed.

        :param path: path to check.
        :return: True if pass filters, false otherwise.
        """
        # indicate if all required filters were matched
        all_required_match = True

        # iterate over filters to match files
        for filt, ftype in self.__filters:

            # handle "Required" filters:
            if all_required_match and ftype == self.FilterType.Required and not filt.match(path):
                all_required_match = False

            # handle "Include" filters:
            elif ftype == self.FilterType.Include and filt.match(path):
                return True

            # handle "Exclude" filters:
            elif ftype == self.FilterType.Exclude and filt.match(path):
                return False

        # if got here it means we processed all filters, and no include/exclude filter was matched.
        # return if all required were matched
        return all_required_match

    def process_file(self, path, dryrun):
        """
        This function is called for every file processed.
        When using this class as an iterator, this function can return None to skip files, or
        process their names before returned.

        :param path: current file path.
        :param dryrun: indicate if we are currently in dry-run mode and should not change files.
        :return: should return filename, or None if you want to omit this file from the iteration loop.
        """
        return path
