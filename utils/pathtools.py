#! python3.13
# coding=utf8

""" some tools for paths"""

__author__ = 'Sihir'
__copyright__ = '© Sihir 2021-2025 all rights reserved'

from os import listdir
from os import walk
from os import environ
from os import getenv
from os import sep as dirsep

from os.path import splitext
from os.path import split
from os.path import isdir
from os.path import isfile
from os.path import basename
from os.path import join
from os.path import abspath

from re import compile as compile_
from typing import Optional

from utils.file_encoding import get_encoding


def has_ext(name: str, ext: str | tuple) -> bool:
    """ return """

    if isinstance(ext, str):
        tup = (ext, )
    elif isinstance(ext, tuple):
        tup = ext
    else:
        return False

    _, cur_ext = splitext(name)
    return cur_ext.lower() in tup


def change_ext(name, ext):
    """ change the extension of a file """
    return f'{splitext(name)[0]}{ext}'


def extension(name: str) -> str:
    """ get the extension of a file """
    _, ext = splitext(name)
    return ext.lower()


def get_folder(filename: str) -> str:
    """ get the folder of a file """
    folder, filename = split(filename)
    return folder


def path_exists(path: str) -> bool:
    """ check whether path exists """
    return isdir(path)


def file_exists(file: str) -> bool:
    """ check whether file exists """
    return isfile(file)


def basename_without_extension(name: str) -> str:
    """ extract the basename from a file """
    result, _ = splitext(basename(name))
    return result


def list_all(cur: str, file_extension: str) -> list:
    """ get all files with the extension in and below the root """
    result = []

    for file in listdir(cur):
        full = join(cur, file)
        if isfile(full):
            if file_extension and extension(file) != file_extension:
                continue
            result.append(full.replace('\\', '/'))

    return result


def list_all_deep(cur: str, file_extension: str = None) -> list:
    """ dive deep """
    result = []
    for root, _, files in walk(cur):
        for file in files:
            if file_extension and extension(file) != file_extension:
                continue

            fullname = join(root, file)
            result.append(fullname)

    return result


def walker(source_path: str, pattern: str, depth: int = -1) -> str:
    """ file name generator """
    regex = compile_(pattern)
    pos = len(source_path)
    for root, _, files in walk(source_path):
        if depth > -1:
            if root[pos:].count(dirsep) >= depth:
                continue

        for file in files:
            if not regex.search(file):
                continue
            yield join(root, file)


def add_file_or_path(file_list: list, file_or_path: str, file_extension: str = '.*') -> list:
    """ used in argument parsing: add a file when the argument is a file
    , else when
    :param file_list: the list to add the file name to
    :param file_or_path: the argument that is either a file name or a path
    :param file_extension: the extension of the files that are searched
    """
    if isfile(file_or_path):
        file_list.append(abspath(file_or_path))
    elif isdir(file_or_path):
        for file in list_all(file_or_path, file_extension):
            file_list.append(file)
    return file_list


def add_from_file(file_list: list, file_name: str) -> list:
    """ read the file with file names in it """

    enc = get_encoding(file_name)
    with open(file_name, encoding=enc) as stream:
        for line in stream:
            file_list.append(line.strip())
    return file_list


def temp_name(base_name: str) -> str:
    """ the file name in the temporary directory """
    path = environ.get("TEMP")
    return join(path, base_name)


def find_path(name: str) -> Optional[str]:
    """ iterate through the PATH environment to find 'name' """
    folders = getenv('PATH').split(';')
    for folder in folders:
        target = join(folder, name)
        if isfile(target):
            return target

    return None
