"""
Cython module for managing a file hierarchy as JSON.
"""

from __future__ import print_function

import os
import errno
import re


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
        self.__root = dirname

    cdef void mkdir(self, char* dirname):
        """Create a directory if not exist."""
        try:
            os.makedirs(dirname)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise RuntimeError(
                    "Could not create directory '{}': {}".format(dirname, e))

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

    cdef void __create_filetree(self, char* root, dict tree_dict,
                                filehandler=None):
        """Create the file system from a dict."""
        for key, val in tree_dict.iteritems():
            filename = re.sub(r"\s+", "-", str(key))
            fullpath = os.path.join(root, filename)
            if isinstance(val, dict):
                # Make the directory, then traverse the dict.
                self.mkdir(fullpath)
                self.__create_filetree(fullpath, val, filehandler=filehandler)
            else:
                # Make the file.
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

