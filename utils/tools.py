#! python3.13

""" the StringBuilder class using StringIO """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

from os import stat
from os import environ

from os.path import splitext

from subprocess import Popen
from subprocess import PIPE

from datetime import datetime

from time import struct_time
from time import localtime
from time import time as _time
from time import sleep

from typing import Optional
from typing import Final

from utils.string_builder import StringBuilder
from utils.quick_sort import quicksort

_DETACHED_PROCESS: Final[int] = 0x00000008


def first(lst: list, default: object = None) -> Optional[object]:
    """ return the first item in the list else return the default for an empty list """
    return None if lst is None else next(iter(lst), default)


def isempty(data: object) -> bool:  # noqa
    """ return True when value is not None and not empty """

    if data is None:
        return True

    if isinstance(data, str):
        result = data.strip()
        return len(result) == 0

    if isinstance(data, list):
        if len(data) == 0:
            return True
        return isempty(first(data, None))

    return True


def discard(lst: list, item: str) -> list:
    """ remove item from list, only if it exists """
    if item in lst:
        lst.remove(item)
    return lst


def str_ellipsis(text: str, width: int) -> str:
    """ use ellipsis, if necessary """
    if text is None:
        text = ''

    if len(text) < width:
        return text

    return f'{text[:width - 4]}... '


def run_detached(cwd: str,
                 program: str,
                 shell=True,
                 args: list = None) -> Popen:
    """ run a program without waiting for the result """

    key = 'PYTHONPATH'  # noqa
    save = environ.get(key, '')
    environ[key] = cwd

    data = [program]
    if args is not None:
        data += args

    # when using 'with', the process will no longer be detached
    # pylint: disable=consider-using-with
    proc = Popen(data,
                 cwd=cwd,
                 shell=shell,
                 stdin=None,
                 stdout=PIPE,
                 stderr=PIPE,
                 close_fds=True)

    sleep(2.0)
    if proc.poll() is None:
        print('micro_player is running')
    else:
        rc = proc.returncode
        out = proc.stdout.read().decode('utf8')
        err = proc.stderr.read().decode('utf8')

        print(f'rc  {rc}')
        print(f'out {out}')
        print(f'err {err}')

    environ[key] = save
    return proc

def to_dhms(value: int) -> str:  # noqa
    """ convert seconds to days:hours:mins:secs """  # noqa

    if value is None:
        return '0:00:00:00'

    minutes = int(value / 60)
    seconds = int(value % 60)
    hours = int(minutes / 60)
    minutes = int(minutes % 60)
    days = int(hours / 24)
    hours = int(hours % 24)

    if days > 0:
        return f'{days}.{hours:0>2}:{minutes:0>2}:{seconds:0>2}'
    else:
        return f'{hours:0>2}:{minutes:0>2}:{seconds:0>2}'


def from_dhms(duration: str) -> int:
    """ calc number of seconds of the track """

    parts = duration.split(':')
    seconds = int(parts[3])
    minutes = int(parts[2])
    hours = int(parts[1])
    days = int(parts[0])
    value = ((24 * days + hours) * 60 + minutes) * 60 + seconds
    return value


def print_dict(vertex: dict, start: int = 2) -> StringBuilder:
    """ what is stored in vertex? """

    builder = StringBuilder()
    if vertex:
        keys = list(vertex.keys())
        quicksort(keys, start=start)

        width = 18
        for key in keys:
            builder.append(f'{key: <{width}}')
            value = vertex[key]
            if isinstance(value, list):
                builder.append_line('[')
                for num, data in enumerate(value):
                    builder.append_line(f'{num: <{width}}{data}')
                builder.append_line(f'{" ":<{width}}]')
            elif isinstance(value, dict):
                result = print_dict(value, start=0).to_string()
                builder.append(result)
            else:
                builder.append_line(f'{value}')
    else:
        builder.append_line('nothing stored in vertex')

    return builder


def timestamp_size(filename: str) -> (str, int):
    """ get the timestamp from the file """

    file_stat = stat(filename)
    tstamp = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y/%m/%d %H:%M')
    return tstamp, file_stat.st_size


def has_ext(filename: str, expected_ext: str) -> bool:
    """ returns True when the extension of the file is the value of ext """

    _, gotten_ext = splitext(filename)
    return gotten_ext.lower() == expected_ext.lower()


def now() -> struct_time:
    """ current date and time """
    return localtime(_time())


def timestamp(when: struct_time) -> str:
    """ create a timestamp string """

    return f'{when.tm_year}' \
           f'{when.tm_mon:0>2}' \
           f'{when.tm_mday:0>2}_' \
           f'{when.tm_hour:0>2}'\
           f'{when.tm_min:0>2}' \
           f'{when.tm_sec:0>2}'
