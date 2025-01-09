#! python3.13

""" connection to the Socket """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

from datetime import timedelta

from typing import Callable

from datetime import datetime

from tkinter import Tk

from player_config import MicroPlayerConfig
from connect_socket import ConnectSocket


class MicroSocket:

    def __init__(self,
                 get_progress: Callable,
                 get_busy: Callable,
                 get_track: Callable,
                 set_sender: Callable,
                 root: Tk):
        """ initialize the class """

        self.get_progress = get_progress
        self.get_busy = get_busy
        self.get_track = get_track
        self.set_sender = set_sender
        self.root = root
        self._last = datetime.now()

        with (cfg := MicroPlayerConfig()):
            value = cfg.value

            self.port = int(value.get('port', '5001'))

        self.connect = ConnectSocket(port=self.port)

    def close(self):
        """ close the connection """
        self.connect.close()

    def update(self):
        """ interpret the message on the socket to get the track to play """

        value = self.get_progress()
        seconds = 0
        if isinstance(value, float):
            seconds = max(0, int(value))

        progress = timedelta(seconds=seconds)

        result = self.connect.poll(self.get_busy(), progress=str(progress))
        if not result:
            # give the sender 5 seconds to reconnect
            if datetime.now() - self._last > timedelta(seconds=5):
                self.set_sender(sender='disconnected')
            return

        self._last = datetime.now()

        value = MicroPlayerConfig().value

        sender = result.get('sender', '')
        if sender:
            self.set_sender(sender=sender)

        fnc = result['function']
        if not fnc:
            return

        match fnc:
            case 'play':
                value['track'] = result['file_name']
                value['progress'] = result['progress']
                self.root.after(200, self.get_track)  # noqa
