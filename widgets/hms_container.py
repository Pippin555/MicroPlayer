#! python3.13
# coding=utf8

""" Spinbox with StringVar """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

from typing import Callable

from tkinter import Frame
from tkinter import Tk
from tkinter import Toplevel
from tkinter import Button

from imgdict.get_dict_img import get_ico

from widgets.spin_box_container import SpinboxContainer


class HmsContainer:
    """ hour minute second triple spin box """

    def __init__(self,
                 master: (Tk, Frame, Toplevel),
                 x_pos: int,
                 y_pos: int,
                 value: tuple,
                 callback: Callable=None):
        """ three connected spin boxes """

        self._window = Toplevel(master)
        self._window.geometry(f'+{x_pos}+{y_pos}')
        self._window.wm_overrideredirect(True)
        self._callback = callback

        state = 'readonly'
        width = 2
        self._hour = SpinboxContainer(master=self._window,
                                      value=0,
                                      min_value=0,
                                      max_value=23,
                                      width=width,
                                      state=state,
                                      carry=self._day_carry_in)

        self._hour.frame.grid(row=0,
                              column=0,
                              padx=0,
                              pady=1,
                              sticky='news')

        self._minute = SpinboxContainer(master=self._window,
                                        value=0,
                                        min_value=0,
                                        max_value=59,
                                        width=width,
                                        state=state,
                                        carry=self._hour.carry_in)

        self._minute.frame.grid(row=0,
                                column=1,
                                padx=0,
                                pady=1,
                                sticky='news')

        self._second = SpinboxContainer(master=self._window,
                                        value=0,
                                        min_value=0,
                                        max_value=59,
                                        width=width,
                                        state=state,
                                        carry=self._minute.carry_in)

        self._second.frame.grid(row=0,
                                column=2,
                                padx=0,
                                pady=1,
                                sticky='news')


        self.icon_check = get_ico(key='check.ico', size=(20, 20))
        self._ok_button = Button(master=self._window,
                                 image=self.icon_check,
                                 command=self._on_ok)

        self._ok_button.grid(row=0,
                             column=3,
                             padx=0,
                             pady=1,
                             sticky='news')

        self.icon_close = get_ico(key='check.ico', size=(20, 20))
        self._cancel_button = Button(master=self._window,
                                     image=self.icon_close,
                                     command=self._close)

        self._cancel_button.grid(row=0,
                                 column=4,
                                 padx=0,
                                 pady=1,
                                 sticky='news')
        self.hms_value = value

    def _day_carry_in(self, amount: int = 0) -> bool:
        """ incoming  carry """

        assert self
        assert amount is not None
        return True

    @property
    def hms_value(self):
        """ return the value """

        return self._hour.value, self._minute.value, self._second.value

    @hms_value.setter
    def hms_value(self, value: tuple):
        """ set the value """

        self._hour.value, self._minute.value, self._second.value = value

    def _on_ok(self):
        """ OK was clicked """

        if self._callback:
            self._callback(self.hms_value)
        self._close()

    def _close(self):
        """""' cancel was clicked """

        self._window.destroy()

    @property
    def frame(self):
        """ the frame of the widget """

        return self._window
