""" VLC music player interface """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2025-2025 all rights reserved'
__version__ = 'Sihir.entertainment.player.v1.0-vlc'  # noqa

from typing import Optional

from queue import Queue

from pathlib import Path

import vlc

from utils.tools import from_dhms


class VlcMixer:
    """ the audio functions (VLC backend) """

    def __init__(self, queue: Queue):
        """ ... """

        self.offset = 0          # milliseconds
        self.duration = 0        # seconds
        self.filename = ''
        self._queue = queue
        self.paused = False

        self._instance = vlc.Instance(
            "--quiet",
            "--aout=directsound")  # noqa

        self._player = self._instance.media_player_new()

        self._event_mgr = self._player.event_manager()
        self._event_mgr.event_attach(
            vlc.EventType.MediaPlayerEndReached,  # noqa
            self._on_end_reached,
        )

    def _on_end_reached(self, event):
        """ ... """

        _ = event

        self.offset = 0
        self.duration = 0
        self.filename = ''
        self.paused = False

        if self._queue is not None:
            self._queue.put(("finished", None))

    def change_progress(self, pos: float):
        """ change the progress by clicking on the progress bar """

        if not self.filename:
            return

        duration = self.duration
        if isinstance(duration, str):
            duration = from_dhms(duration)

        seconds = int(duration * pos)
        self.offset = seconds * 1000
        self._player.set_time(self.offset)

    def get_progress(self) -> Optional[float]:
        """ at how many seconds is the player """

        state = self._player.get_state()
        if state in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):  # noqa
            return None

        pos_ms = self._player.get_time()
        if pos_ms < 0 or self._player.get_length() <= 0:
            return None

        value = pos_ms / 1000.0
        return value

    @property
    def busy(self) -> int:
        """
        returns:
            0 when stopped
            1 when playing
            2 when paused
        """

        state = self._player.get_state()

        match state:
            case vlc.State.Playing:  # noqa
                self.paused = False
                return 1
            case vlc.State.Paused:  # noqa
                return 2
            case _:
                return 0

    def load(self, track: str, duration: int, progress: int):
        """ load and play the track """

        path = Path(track)
        if not path.exists():
            raise FileNotFoundError(path)

        self.duration = duration
        self.filename = track

        if progress is None or isinstance(progress, str):
            progress = 0.0

        self.offset = int(progress * 1000)

        media = self._instance.media_new(path.as_uri())
        self._player.set_media(media)
        self._player.play()

        if self.offset > 0:
            self._player.set_time(self.offset)

    def play(self) -> str:
        """ play or pause """

        state = self._player.get_state()

        if state == vlc.State.Playing:  # noqa
            self._player.pause()
            self.paused = True
            return 'play'

        self._player.play()
        return 'pause'

    def stop(self):
        """ stop the music """

        self._player.stop()
        self.unload()

    def reposition(self, value: tuple):
        """ change the progress """

        hour, minute, second = value
        seconds = second + 60 * (minute + 60 * hour)

        self.offset = seconds * 1000
        self._player.set_time(self.offset)

    def unload(self):
        """ release the file """

        self._player.stop()
        self.filename = ''
