""" Checkbutton container """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

from typing import Callable

from tkinter import Tk
from tkinter import Toplevel
from tkinter import Frame
from tkinter import Radiobutton
from tkinter import IntVar


class RadioButtonsContainer:
    """ container for a Checkbutton """

    def __init__(self,
                 master: (Tk | Toplevel | Frame),
                 **kwargs):

        """ initialize the RadiobuttonContainer """

        self._frame = Frame(master)
        radios: [(str, int, int, int)] = kwargs.get('radios', [])
        state = kwargs.get('state', '')
        width = kwargs.get('width', 10)
        callback: Callable = kwargs.get('callback', None)

        self.rad_var = IntVar(
            master=self._frame,
            value=state)

        if callback is not None:
            self.rad_var.trace('w', callback)

        self.controls = []

        for text, value, row, column in radios:
            rad_button = Radiobutton(
                master=self._frame,
                text=text,
                width=width,
                value=value,
                justify='left',
                variable=self.rad_var)

            rad_button.grid(row=row,
                            column=column,
                            padx=1,
                            pady=1,
                            sticky='w')
            self.controls.append(rad_button)

    @property
    def state(self) -> int:
        """ which radiobutton is selected? """

        return self.rad_var.get()

    @state.setter
    def state(self, value: bool):
        """ whether the checkbox is checked or not """

        self.rad_var.set(value=value)

    @property
    def frame(self):
        """ return the checkbutton and the container """

        return self._frame
