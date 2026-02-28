""" the GUI for the query """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa
__version__ = 'Sihir.entertainment.player.v1.0'  # noqa

from tkinter import Tk
from tkinter import Frame
from tkinter import Toplevel
from tkinter import Listbox
from tkinter import Label
from tkinter import StringVar


class ListboxContainer:
    """ container for a multiselect listbox """

    def __init__(self,
                 master: (Tk | Toplevel),
                 **kwargs):
        """ initialize the class """

        self._frame = Frame(master)
        text = kwargs.get('text', '')
        width = kwargs.get('labelwidth', 10)  # noqa
        height = kwargs.get('listheight', 5)  # noqa
        multi_select = kwargs.get('multi_select', True)

        self.lst_label = Label(master=self._frame,
                               width=width,
                               justify='left',
                               anchor='nw',
                               text=text)

        self.lst_label.grid(row=0,
                            column=0,
                            rowspan=height,
                            padx=2,
                            pady=0,
                            sticky='news')

        mode = 'multiple' if multi_select else 'single'

        self.str_var = StringVar()

        self.lst_box = Listbox(master=self._frame,
                               justify='left',
                               selectmode=mode,
                               height=height,
                               exportselection=False,
                               listvariable=self.str_var)

        self.lst_box.grid(row=0,
                          column=1,
                          padx=1,
                          pady=0,
                          sticky='news')

        values = kwargs.get('values', [])
        self.str_var.set(values)

        width = 20
        for value in values:
            width = max(width, len(value) + 1)

        self.lst_box.config(width=width)

    @property
    def frame(self):
        """ return the frame """

        return self._frame

    def selected_indices(self) -> []:
        """ return the selected indices """

        return self.lst_box.curselection()

    def selected_values(self) -> []:
        """ return the selected values """

        return [self.lst_box.get(i) for i in self.lst_box.curselection()]
