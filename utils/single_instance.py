""" receive the system event when the program is the only instance, else None """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2025 all rights reserved'  # noqa

from sys import argv

from os.path import basename
from os.path import splitext

from typing import Optional

from utils.system_event import SystemEvent


def single_instance() -> (Optional[SystemEvent], str):
    """
    only allow one instance
    param script_name: the file name of the main script file
    usage:

    inst, name = single_instance()

    if not inst:
        print(f 'only one instance of {name} is allowed')
        exit(non-zero)

    the main program needs to hold 'inst' until it exits
    """

    pgm_name, _ = splitext(basename(argv[0]))

    instance = SystemEvent(name=pgm_name)
    return instance if instance.owner else None, pgm_name
