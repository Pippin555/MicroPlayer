#! python3.13
# coding=utf8

""" receive the system event when the program is the only instance, else None """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

from os.path import splitext

from typing import Optional

from utils.system_event import SystemEvent


def single_instance(event_name: str) -> (Optional[SystemEvent], str):
    """
    only allow one instance
    param script_name: the file name of the main script file
    usage:

    inst, name = single_instance(basename(argv[0]))

    if not inst:
        print(f 'only one instance of {name} is allowed')
        exit(non-zero)
    """

    name, _ = splitext(event_name)
    instance = SystemEvent(name=name)
    return instance if instance.owner else None, name
