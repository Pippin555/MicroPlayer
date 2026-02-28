""" show a popup window """

__author__ = 'Sihir'  # noqa
__copyright__ = "© Sihir 2023-2024 all rights reserved"  # noqa

from os.path import splitext

from tkinter import Tk
from tkinter import Label
from tkinter import Frame
from tkinter import Menu
from tkinter import Button
from tkinter import Toplevel
from tkinter import Listbox

from typing import Callable
from typing import Optional

from functools import partial

from widgets.dialog_result import DialogResult

from imgdict.get_dict_img import get_ico


# the INLINE version
class Popup:
    """ simple popup """

    def __init__(self, root, **kwargs):
        """ show a message """

        assert root
        self.root = root
        title = kwargs.get('title', 'Popup')
        self.root.title(title)

        basename, _ = splitext(__file__)
        self._icon = get_ico(key='popup.ico', size=(20, 20))
        self.root.iconphoto(False, self._icon, self._icon)  # noqa _PhotoImageLike can't be referenced

        self.root.protocol("WM_DELETE_WINDOW", self.exit_script)
        self.root.bind('<Escape>', self.escape_key)
        self.root.bind('<Return>', self.enter_key)
        self._dialog_close = kwargs.get('dialog_close', None)

        self._popup_info = kwargs.get('popup_info', None)
        self._dialog_result = DialogResult.CLOSE_WINDOW
        self._tag = kwargs.get('tag', None)

        root.bind('<Configure>', self._on_form_event)
        position = kwargs.get('position', None)
        if position is not None:
            self._window_left, self._window_top = position
            self.root.geometry(f'+{self._window_left}+{self._window_top}')
        else:
            self._window_left = 100
            self._window_top = 100

        self._callback: Optional[Callable] = kwargs.get('callback', None)

        self.message = kwargs.get('message', 'Nothing to report')
        family = kwargs.get('font_family', 'Times New Roman')
        font = (family, 10)
        width, height = kwargs.get('size', (len(self.message), 1))

        main = Frame(self.root)
        mode = kwargs.get('mode', 'label')
        match mode:
            case 'label':
                self.label = Label(master=main,
                                   text=self.message,
                                   font=font,
                                   justify='left')
                self.label.configure(width=width,
                                     height=height,
                                     anchor='w')
                self.label.grid(row=0,
                                column=0,
                                columnspan=2,
                                padx=2,
                                pady=2,
                                sticky='news')

            case 'list':
                self.list = Listbox(master=main,
                                    font=font,
                                    width=width,
                                    height=height)

                self.list.grid(row=0,
                               column=0,
                               columnspan=2,
                               padx=2,
                               pady=2,
                               sticky='news')

                self.list.bind('<Double-1>', self._list_click)
                lines = self.message.split('\n')
                for index, line in enumerate(lines):
                    self.list.insert(index, line)

                self.list.bind('<Button-3>', self._right_click)

        ok_button = Button(master=main,
                           text="OK",
                           width=6,
                           command=self.ok_click,
                           fg='white',
                           bg='blue')

        ok_button.grid(row=1,
                       column=0,
                       padx=20,
                       pady=(2, 6),
                       sticky='w')

        cancel_button = Button(master=main,
                               text="Cancel",
                               width=6,
                               command=self.cancel_click,
                               fg='white',
                               bg='blue')

        cancel_button.grid(row=1,
                           column=1,
                           padx=20,
                           pady=(2, 6),
                           sticky='e')

        seconds = kwargs.get('seconds', None)
        if seconds is not None:
            self._dialog_result = DialogResult.EXPIRED
            self.root.after(1000 * seconds, self.destroy)

        self.on_exit = kwargs.get('on_exit', None)

        main.grid(row=0, column=0, sticky='news')
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # prevent the garbage collect tp removed these
        # and also pylint yapping about too manu instance variables
        self.layout = {
            'ok': ok_button,
            'cancel': cancel_button
        }

    def _on_form_event(self, event):
        """ something changed in the windows form """

        if event.type == '22':
            # size or position changed
            self._window_left = event.x
            self._window_top = event.y

    @property
    def window_left(self) -> int:
        """ return the window position """

        return self._window_left

    @property
    def window_top(self) -> int:
        """ return the window top position """

        return self._window_top

    def _list_click(self, event):
        """ the list was clicked """

        # Note here that Tkinter passes an event object to _list_click
        list_widget = event.widget
        index = int(list_widget.curselection()[0])
        line = list_widget.get(index)
        # print(f'You selected item {index}: {line}')
        if self._callback is not None:
            self._callback(sender=self, index=index, line=line)

    def _right_click(self, event):
        """ right click on the list """

        list_widget = event.widget
        index = list_widget.nearest(event.y)

        menu = Menu(master=self.root,
                    tearoff=False)

        if self._popup_info is None:
            return

        for item in self._popup_info:
            name, cmd = item
            line = list_widget.get(index)
            menu.add_command(label=name, command=partial(cmd, line))

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def ok_click(self):
        """ OK button clicked """

        self._dialog_result = DialogResult.OK
        self.destroy()

    def cancel_click(self):
        """ cancel button clicked """

        self._dialog_result = DialogResult.CANCEL
        self.destroy()

    def escape_key(self, event_args):
        """ escape was clicked """

        assert event_args
        self._dialog_result = DialogResult.ESCAPE
        self.destroy()

    def enter_key(self, event_args):
        """ escape was clicked """

        assert event_args
        self._dialog_result = DialogResult.ENTER
        self.destroy()

    def exit_script(self):
        """ destroy the master """

        self._dialog_result = DialogResult.CLOSE_WINDOW
        self.destroy()

    def destroy(self):
        """ the popup window is destroyed """

        if self._dialog_close is not None:
            self._dialog_close(sender=self, result=self._dialog_result)

        if self.on_exit is not None:
            self.on_exit()

    @property
    def dialog_result(self):
        """ return the dialogResult """

        return self._dialog_result

    @property
    def dialog_close_event(self) -> Callable:
        """ property of the dialog close event """

        return self._dialog_close

    @dialog_close_event.setter
    def dialog_close_event(self, value: Callable):
        """ setter for the dialog close event """

        self._dialog_close = value

    @property
    def tag(self) -> object:
        """ property of the dialog tag """

        return self._tag

    @tag.setter
    def tag(self, tag: object):
        """ setter for the dialog close event """

        self._tag = tag


class PopupWindowed(Popup):
    """ for use as sub-window in tkinter environment """

    def __init__(self, root=None, **kwargs):
        """ initialize the Popup """

        alone = root is None
        self.new_root = Tk() if alone else Toplevel(root)
        super().__init__(root=self.new_root, **kwargs)
        self.on_exit = self.destroy_toplevel
        if alone:
            self.new_root.mainloop()

    def destroy_toplevel(self):
        """ remove the Toplevel """

        self.new_root.destroy()


class PopupStandalone(PopupWindowed):
    """ for use in non-tkinter environment """


def ellipse(file_name: str, width=30) -> str:
    """ shorten a long file name """

    if len(file_name) < width:
        return file_name

    parts = file_name.replace('/', '\\').split('\\')
    if len(parts) > 4:
        return '\\'.join((*parts[:2], '...', *parts[-2:]))

    return file_name
