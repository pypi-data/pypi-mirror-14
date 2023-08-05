#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    dropbox_tools/dropbox_tools.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A collection of CRUD operations for Dropbox.

"""

import dropbox

def upload_file(filename):
    """ Uploads a single file to a Dropbox account.

    Keyword arguments:
    filename -- Path and name of the file to upload to Dropbox.

    """

    pass

def upload_files(file_path):
    """ Uploads multiple files to a Dropbox account.

    Keyword arguments:
    file_path -- Path to the files to upload.
    """

    pass

def upload_directory(directory_path):
    """ Uploads a directory to a Dropbox account, creating the directory in the
        process.

    Keyword arguments:
    directory_path -- Path and name of directory to upload.
    """

    pass

def list_files():
    """ List all files in a specified Dropbox account.
    """

    pass

def list_directory(directory_path):
    """ List the contents of a directory stored in a Dropbox folder.

    Keyword arguments:
    directory_path -- Path and name of directory to upload.
    """
    pass

def delete_file(filename):
    """ Deletes a specified file from a user's Dropbox account.

    Keyword arguments:
    filename -- Name of file to delete from Dropbox account.
    """
    pass

def delete_files(file_path):
    """ Delete all files from a specified directory in a user's Dropbox account.

    Keyword arguments:
    file_path -- Path on Dropbox where the files are located.
    """

    pass

def delete_directory(directory_path):
    """ Delete a directory an its contents from a user's Dropbox account.

    Keyword arguments:
    directory_path -- Path on Dropbox where the directory is located.
    """

    pass



