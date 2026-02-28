""" the class that handles the SystemEvent API """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

# pip install pywin32
# these functions are not exposed to pylint:
# pylint: disable=no-name-in-module
from win32api import GetLastError as _GetLastError
from win32api import CloseHandle

from win32event import CreateEvent as _CreateEvent
from win32event import WaitForSingleObject as _WaitForSingleObject
from win32event import SetEvent as _SetEvent
from win32event import ResetEvent as _ResetEvent
from win32event import WAIT_OBJECT_0 as _WAIT_OBJECT_0
# pylint: enable=no-name-in-module


class SystemEvent:
    """ can be used to synchronise processes """

    def __init__(self, name: str):
        """ initialize the SystemEvent class """

        self._handle = _CreateEvent(None,  # EventAttributes
                                    True,  # ManualReset
                                    True,  # InitialState
                                    name)  # name

        self._create_error = _GetLastError()

    @property
    def owner(self) -> bool:
        """ True when the caller is now the owner of the event """

        return self._create_error == 0

    @property
    def state(self) -> bool:
        """ return the state """

        return _WaitForSingleObject(self._handle, 1) == _WAIT_OBJECT_0

    @state.setter
    def state(self, value: bool):
        """ set the state, anyone with access to this state can read or write it """

        if value:
            _SetEvent(self._handle)
        else:
            _ResetEvent(self._handle)

    def __enter__(self):
        """ with statement entered """

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ with statement exited """

        if self._handle:
            CloseHandle(self._handle)
