#! python3.13
""" deduce the file encoding from the Byte Order Mark or the file contents """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2021-2024 all rights reserved'

from os.path import isfile
from os.path import getsize

from typing import Optional

# pip install chardet
import chardet


def get_encoding(filename: str) -> Optional[str]:
    """ get the byte order mark from the file, if any and deduce the encoding """
    if isfile(filename) and getsize(filename) > 1:
        with open(filename, 'rb') as stream:
            contents = stream.read()

        return get_str_encoding(contents)

    return "UTF-8-SIG"


def get_str_encoding(contents: bytes) -> str:
    """ deduce the encoding of the value """
    det = chardet.detect(contents)
    if det['confidence'] > 0.3:
        return det['encoding']

    return "UTF-8-SIG"
