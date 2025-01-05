#! python3.13
# coding=utf8

""" the helper for the Popup window """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa
__version__ = 'Sihir.entertainment.player.v1.0'  # noqa

from tkinter import Tk

from typing import Callable
from typing import Optional

from utils.string_builder import StringBuilder

from widgets.popup import PopupWindowed
from widgets.popup import DialogResult


class PopupHelper:
    """ help for popup """
    def __init__(self,
                 list_callback: Callable,
                 dialog_close: Callable,
                 window_left: int = 100,
                 window_top=100,
                 tag=None):
        """ help for popup """

        self.saved_pop = None
        self.window_left = window_left
        self.window_top = window_top
        self._list_callback = list_callback
        self._dialog_close = dialog_close
        self._tag = tag

    def do_popup(self, **kwargs):
        """ show a popup from the builder """

        builder: Optional[StringBuilder] = kwargs.get('builder', None)
        root: Optional[Tk] = kwargs.get('root', None)
        mode: str = kwargs.get('mode', 'list')
        tag: Optional[str] = kwargs.get('tag', None)
        seconds: Optional[int] = kwargs.get('seconds', None)
        popup_info: [tuple] = kwargs.get('popup_info', None)

        popup = self.saved_pop
        if popup is not None:
            popup.destroy()
            self.saved_pop = None

        if len(str(builder)) == 0:
            return

        count = builder.count_lines()
        height = min(40, max(1, count))
        width = 20
        message = str(builder)
        for line in message.split('\n'):
            width = max(width, len(line))

        popup = PopupWindowed(root=root,
                              message=str(builder),
                              mode=mode,
                              callback=self._list_callback,
                              dialog_close=self._dialog_close,
                              font_family='Courier New',
                              position=(self.window_left, self.window_top),
                              size=(width + 1, height + 1),
                              seconds=seconds,
                              tag=tag if tag else self._tag,
                              popup_info=popup_info)

        self.saved_pop = popup

    def _dialog_closing(self, sender: PopupWindowed, dialog_result: DialogResult):
        """ save the current location """
        self.window_left = sender.window_left
        self.window_top = sender.window_top

        if self._dialog_close is not None:
            self._dialog_close(sender, dialog_result)

    def hide_popup(self):
        """ hide the popup """
        if self.saved_pop is None:
            return
        self.saved_pop.destroy()
