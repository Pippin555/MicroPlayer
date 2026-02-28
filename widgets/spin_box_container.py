""" Spinbox with StringVar """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

from tkinter import Tk
from tkinter import Toplevel
from tkinter import Frame
from tkinter import StringVar
from tkinter import Spinbox


class SpinboxContainer:
    """ the container for a Spinbox """

    def __init__(self, master: (Tk, Toplevel, Frame), **kwargs):
        """ initialize the container """

        self.master = master
        min_value = kwargs.get('min_value', 0)
        max_value = kwargs.get('max_value', 100)
        carry = kwargs.get('carry', None)
        state = kwargs.get('state', 'readonly')

        self.cfg = {
            'min_value': min_value,
            'max_value': max_value,
            'carry': carry,
        }

        value = kwargs.get('value', min_value)
        if bool(kwargs.get('carry', False)):
            min_value -= 1
            max_value += 1

        self.string_var = StringVar(
            master=master,
            value=str(value))

        self.width = kwargs.get('width', 2)

        self.spin = Spinbox(
            master=master,
            textvariable=self.string_var,
            from_=min_value,
            to=max_value,
            width=self.width,
            state=state,
            readonlybackground='lightgray')

        self.name = kwargs.get('name', str(self.string_var))

        # do not call back before everything is initialized
        self.changed = kwargs.get('changed', None)
        if self.changed:
            self.changed(self.name, self.value)
        self.string_var.trace('w', self._str_var_callback)

    @property
    def value(self):
        """ current value """

        return int(self.string_var.get())

    @value.setter
    def value(self, data: int):
        """ new value """

        val = f'{int(data):0>{self.width}}'
        self.string_var.set(val)

    def _str_var_callback(self, *kwargs):
        """ the value has changed """

        assert kwargs
        try:
            new_value = int(self.string_var.get())
        except ValueError:
            # there is an intermediate state
            return

        self._handle_carry(new_value)
        if self.changed:
            self.changed(name=self.name, value=self.value)

    def _handle_carry(self, value: int) -> bool:
        """ process carry """

        max_value = self.cfg['max_value']
        min_value = self.cfg['min_value']
        carry = self.cfg['carry']

        result = True
        if value > max_value:
            if carry and carry(1):
                self.value = min_value
            else:
                self.value = max_value
                result = False

        elif value < min_value:
            if carry and carry(-1):
                self.value = max_value
            else:
                self.value = min_value
                result = False

        else:
            self.value = value
        return result

    def carry_in(self, amount: int) -> bool:
        """ process carry """

        value = self.value + amount
        return self._handle_carry(value)

    @property
    def frame(self) -> Spinbox:
        """ return the spin and the frame """

        return self.spin

    @property
    def max(self) -> int:
        """ maximum value """

        return self.cfg['max_value']

    @property
    def min(self) -> int:
        """ minimum value """

        return self.cfg['min_value']
