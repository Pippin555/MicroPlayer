#! python3.13
# coding=utf8

""" the container for an entry with prompt and unit labels """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

from typing import Optional
from typing import Callable

from tkinter import Label
from tkinter import Toplevel
from tkinter import Frame
from tkinter import Entry
from tkinter import StringVar


class EntryContainer:
    """ entry and its StringVar """
    def __init__(self,
                 master: [Frame | Toplevel],
                 **kwargs):
        """ initialize the Label, Entry and StringVar """

        frame = Frame(master=master)

        prompt = kwargs.get('prompt', '')
        label_prompt = Label(master=frame,
                             width=kwargs.get('prompt_width', 50),
                             text=prompt,
                             anchor='w',
                             justify='left')

        label_prompt.grid(row=0,
                          column=0,
                          padx=2,
                          pady=2,
                          sticky='news')

        str_value = StringVar(master=frame,
                              value=kwargs.get('value', ''))

        self.tag = kwargs.get('tag', None)
        if self.tag is None:
            self.tag = prompt

        entry = Entry(master=frame,
                      width=kwargs.get('width', 10),
                      textvariable=str_value)

        entry.grid(row=0,
                   column=1,
                   padx=2,
                   pady=2,
                   sticky='news')

        unit_width = kwargs.get('unit_width', 0)
        unit_text = kwargs.get('unit_text', '')

        self.label_unit = Label(master=frame,
                                width=unit_width,
                                text=unit_text)

        self.label_unit.grid(row=0,
                             column=2,
                             padx=2,
                             pady=2,
                             sticky='news')

        self.setup = {'frame': frame,
                      'prompt': label_prompt,
                      'value': str_value,
                      'entry': entry,
                      'unit': self.label_unit}

        frame.grid(row=0,
                   column=0,
                   padx=2,
                   pady=2,
                   sticky='news')

        on_return: Optional[Callable] = kwargs.get('on_return', None)
        if on_return is not None:
            entry.bind('<Return>', on_return)

        on_leave: Optional[Callable] = kwargs.get('on_leave', None)
        if on_leave is not None:
            entry.bind('<FocusOut>', on_leave)

    @property
    def frame(self) -> Frame:
        """ return the frame """

        return self.setup['frame']

    @property
    def value(self) -> str:
        """ return the value """

        str_value = self.setup['value']
        return str_value.get()

    @value.setter
    def value(self, data: str):
        """ set the value """

        str_value = self.setup['value']
        str_value.set(data)

    @property
    def unit(self):
        """ the unit of the value """

        return self.label_unit.cget('text')

    @unit.setter
    def unit(self, value: str):
        """ set the unit """

        self.label_unit.config(text=value)
