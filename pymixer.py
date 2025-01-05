#! python3.13
# coding=utf8

""" pygame music player interface """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa
__version__ = 'Sihir.entertainment.player.v1.0'  # noqa

from typing import Optional
from typing import Callable

from datetime import timedelta

# pip install pygame
# pylint: disable=no-name-in-module
from pygame import init as _game_init
from pygame.mixer import init as _mixer_init
from pygame.mixer import music as _music
from pygame import USEREVENT
from pygame import event as _game_event
# pylint: enable=no-name-in-module

from utils.tools import from_dhms


class PyMixer:
    """ the audio functions """
    END_EVENT = USEREVENT + 1

    def __init__(self, finished: Callable):
        """ initialize the class """
        self.offset = 0
        self.duration = 0
        self.filename = ''
        self.finished = finished
        self.paused = False

        _game_init()
        _mixer_init()
        _music.set_endevent(PyMixer.END_EVENT)

    @property
    def progress(self) -> str:
        """ return the current progress """

        delta = int(_music.get_pos() / 1000)
        return str(timedelta(seconds=delta))

    def change_progress(self, pos: float):
        """ change the progress by clicking on the progress bar """

        if _music.get_busy():
            filename = self.filename
            duration = self.duration

            if isinstance(duration, str):
                duration = from_dhms(duration)

            pos = int(duration * pos)
            self.offset = pos * 1000
            _music.load(filename)
            _music.play(start=pos)

    def get_progress(self) -> Optional[float]:
        """ at how many seconds is the player """

        pos = _music.get_pos()

        for event in _game_event.get():
            if event.type == PyMixer.END_EVENT:
                self.offset = 0
                self.duration = 0
                self.filename = ''

                if self.finished is not None:
                    self.finished()

                return None

        return (pos + self.offset) / 1000

    @property
    def busy(self) -> int:
        """
        returns:
            0 when stopped
            1 when playing
            2 when paused
        """

        result = 0
        match _music.get_busy():
            case False:
                if self.paused:
                    result = 2
            case True:
                self.paused = False
                result = 1

        return result

    def load(self, track: str, duration: int, progress: int):
        """ load and play the track"""

        self.duration = duration
        self.filename = track
        if progress is None or isinstance(progress, str):
            progress = 0.0
        self.offset = 1000.0 * progress

        _music.load(track)
        _music.play(start=progress)

    def play(self) -> str:
        """ play of pause """

        assert self is not None

        if _music.get_busy():
            _music.pause()
            self.paused = True
            return 'play'

        _music.unpause()
        return 'pause'

    def stop(self):
        """ stop the music """

        _music.stop()
        self.unload()

    def reposition(self, value: tuple):
        """ change the progress """

        hour, minute, second = value
        pos = second + 60 * (minute + 60 * hour)
        self.offset = 1000 * pos
        _music.play(start=pos)

    def unload(self):
        """ release the file """

        assert self  # do not want to make an exception for this function

        _music.unload()
