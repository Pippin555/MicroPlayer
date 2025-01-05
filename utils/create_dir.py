#! python3.13

""" create directory and create directory for a file """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2021-2024 all rights reserved'

from os import mkdir
from os.path import dirname
from os.path import exists
from os.path import isdir


def create_dir(full_path: str) -> bool:
    """ create a directory whether it already exists or not """
    if exists(full_path):
        return True

    paths = [full_path]
    while True:
        # go up a parent to find an existing path
        full_path = dirname(full_path)
        if exists(full_path):
            break
        # save then non-existing path to the list
        paths.insert(0, full_path)

    # create the directories in reversed order
    for path in paths:
        mkdir(path)

    return True


def create_dir_for(file_name: str) -> None:
    """ create the directory for file_name """
    path = dirname(file_name)
    if isdir(path):
        return
    create_dir(path)
