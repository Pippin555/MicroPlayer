#! python3.13
# coding=utf8

""" the business part of the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

from typing import Optional
from typing import Callable
from typing import Any

from re import compile as _compile

from utils.string_builder import StringBuilder
from utils.tools import str_ellipsis

from mp3.mp3tags import Mp3Tags

from player_config import MicroPlayerConfig

from popup_helper import PopupHelper
from popup_helper import PopupWindowed
from popup_helper import DialogResult


# pylint: disable=too-many-public-methods
class PyPlayerBusiness:  # pylint: disable=too-many-instance-attributes
    """ the business class of the player """

    def __init__(self):
        """ initialize the business class """

        self._root = None
        self._data_folder = None
        self._extension = None
        self._patt = _compile(r'] *(\d+) ')
        self._popup_helper = None
        self.play_track: Optional[Callable] = None
        self._result_callback = None
        self._list = []

    @property
    def extension(self) -> str:
        """ get the file extension """

        return self._extension

    @extension.setter
    def extension(self, value: str):
        """ set the file extension """

        self._extension = value

    def set_play_track(self, callback: Callable) -> None:
        """ set the function to get a random track """

        self.play_track = callback

    def start(self):
        """ start the player """

        if self.play_track is not None:
            self.play_track()

    @staticmethod
    def show_track(track: Mp3Tags):
        """ return string representation of the mp3 """

        ident = track.id
        artist = str_ellipsis(track.artist, 25)
        composer = str_ellipsis(track.composer, 25)
        title = str_ellipsis(track.title, 40)
        return f'{ident: >6} - {artist} - {composer} - {title}'

    @property
    def popup_helper(self):
        """ get the popup helper """

        if self._popup_helper is None:
            conf = MicroPlayerConfig().value
            window_left, window_top = conf.get('position', (100, 100))

            self._popup_helper = \
                PopupHelper(list_callback=self._list_callback,
                            dialog_close=self._dialog_close,
                            window_top=window_top,
                            window_left=window_left)
        return self._popup_helper

    def do_popup(self, **kwargs):
        """ show a popup from the builder """

        builder: StringBuilder = kwargs.get('builder', None)
        mode: str = kwargs.get('mode', 'list')
        tag: Any = kwargs.get('tag', None)
        seconds: Optional[int] = kwargs.get('seconds', None)
        # has_context = kwargs.get('has_context', False)

        helper = self.popup_helper

        if len(str(builder)) == 0:
            if helper is not None:
                helper.hide_popup()
            return

        context_info = None
        helper.do_popup(builder=builder,
                        root=self._root,
                        mode=mode,
                        tag=tag,
                        seconds=seconds,
                        popup_info=context_info)

    def _dialog_close(self, sender: PopupWindowed, result: DialogResult):
        """ dialog is closing """

        assert self
        assert result

        position = (sender.window_left, sender.window_top)
        with (conf := MicroPlayerConfig()):
            conf.value['position'] = position

    # @deprecated(reason='no longer supported')
    def _list_callback(self, sender: Any, index: int, line: str):
        """ line is the clicked line """

    # @deprecated(reason='save_progress needs a new implementation')
    def save_progress(self, index: int, progress: int):
        """ save the progress in the DB """

    @property
    def result_callback(self) -> Callable:
        """ for getting the result callback function """
        return self._result_callback

    @result_callback.setter
    def result_callback(self, value: Callable):
        """ for setting the result callback function """
        self._result_callback = value

    def db_callback(self, req: dict):
        """ message from the database """

        for key, value in req:
            print(f'{key: <8} {value}')
