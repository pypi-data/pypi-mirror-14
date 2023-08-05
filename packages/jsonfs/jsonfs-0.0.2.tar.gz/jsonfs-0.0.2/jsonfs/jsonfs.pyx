"""
Cython module for managing a file hierarchy as JSON.
"""

from __future__ import print_function

import os
import errno
import re

from libc.stdlib cimport malloc, free
from libc.string cimport strncpy


cdef class Directory(dict):
    """Class representing a file hierarchy as a dictionary."""

    cdef char* __root

    def __init__(self, char* dirname):
        """Populate the dictionary from the directory."""
        # Create the dir
        if not os.path.isdir(dirname):
            self.mkdir(dirname)

        # Populate the tree
        self.__parse_dir(dirname, self)

        # Set properties
        self.__root = <char*>malloc(len(dirname) * sizeof(char))
        if not self.__root:
            raise MemoryError()
        strncpy(self.__root, dirname, len(dirname))

    def __dealloc__(self):
        free(self.__root)

    cdef void mkdir(self, char* dirname):
        """Create a directory if not exist."""
        try:
            os.makedirs(dirname)
        except OSError as e:
            if e.errno != errno.EEXIST:
                # Allow for this to pass.
                pass

    cdef void __parse_dir(self, char* dirname, dict tree_dict,
                          filehandler=None):
        """Convert the file system to a dict."""
        for filename in os.listdir(dirname):
            fullpath = os.path.join(dirname, filename)
            if os.path.isdir(fullpath):
                # Recursively call function if directory.
                # Make this file a dict.
                tree_dict[filename] = {}
                self.__parse_dir(fullpath, tree_dict[filename],
                                 filehandler=filehandler)
            elif os.path.isfile(fullpath):
                # Stoping condition is if file is a file.
                # If filehandler is provided, the result of passing the
                # fullpath to it will be the value. Otherwise, it will just
                # be the fullpath itself.
                if hasattr(filehandler, "__call__"):
                    tree_dict[filename] = filehandler(fullpath)
                else:
                    tree_dict[filename] = fullpath

    cdef bint __spelled_like_dir(self, char* filename):
        """Check if a file is spelle like a dir (ends with os.sep)."""
        return filename.endswith(os.sep)

    cdef void __create_filetree(self, char* root, dict tree_dict,
                                filehandler=None):
        """Create the file system from a dict."""
        for key, val in tree_dict.iteritems():
            filename = str(key)
            fullpath = os.path.join(root, filename)
            if isinstance(val, dict):
                # Make the directory, then traverse the dict.
                self.mkdir(fullpath)
                self.__create_filetree(fullpath, val, filehandler=filehandler)
            else:
                # Make the file.
                # Do not attempt to make files that are dirs
                if self.__spelled_like_dir(fullpath):
                    continue

                open(fullpath, "a").close()

                # Do something with the file.
                if hasattr(filehandler, "__call__"):
                    filehandler(fullpath)

    cpdef void reload(self, filehandler=None):
        """Reload the filesystem."""
        self.__parse_dir(self.__root, self, filehandler=filehandler)

    cpdef void commit(self, filehandler=None):
        """Commit changes to filesystem."""
        self.__create_filetree(self.__root, self, filehandler=filehandler)

