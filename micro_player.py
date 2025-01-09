#! python3.13

""" the GUI for the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2025 all rights reserved'  # noqa

from sys import exit as _exit
from sys import argv

from time import sleep

from typing import Callable

from os.path import isfile

from utils.repeating_timer import RepeatTimer

from gui import PyPlayerGui
from business import PyPlayerBusiness
from player_config import MicroPlayerConfig

from micro_socket import MicroSocket


# pylint: disable=too-few-public-methods
class MicroPlayer:
    """ my player """

    def __init__(self):
        """ initialize the class """

        value = {}
        self.use_socket = False
        self.use_gremlin = False
        self.updates: [Callable] = []
        self.connection = None

        port = 5001
        with (cfg := MicroPlayerConfig(main=__file__, value=value)):
            value = cfg.value
            if 'port' not in value:
                value['port'] = str(port)

            track = value.get('track', None)
            if not isfile(track):
                value['track'] = "C:\\bin\\Boenda Moelia II.mp3"

            it_arg = iter(argv[1:])
            for arg in it_arg:
                match arg:
                    case '-m':
                        value['track'] = next(it_arg, None)

                    case '-p':
                        str_port = next(it_arg, str(port))
                        value['port'] = str_port
                        port = int(str_port)

        self.business = PyPlayerBusiness()
        self.gui = PyPlayerGui(business=self.business,
                               track_selected=self.select_track)

        self.updates.append(self.gui.get_progress)

        self.gui.create_gui()

        # save the root
        self.business.root = self.gui.root

        self.gui.start(autostart=True)

        self.connection = MicroSocket(
            get_progress=self.gui.get_progress,
            get_busy=self.gui.get_busy,
            get_track=self.business.play_track,
            set_sender=self.set_sender,
            root=self.gui.root)

        self.updates = self.connection.update

        timer = RepeatTimer(
            interval=1.0,
            function=self.updates)
        timer.start()

        self.gui.run()

        if self.connection:
            self.connection.close()

        timer.cancel()

        sleep(2)

    def set_sender(self, sender: str):
        """ who sent the message? """

        self.gui.set_sender(sender=sender)

    def select_track(self, file_name: str):
        """ select the track to play """

        if file_name == '-q':
            if self.connection:
                self.connection.close()
                self.connection = None
            return

        with (cfg := MicroPlayerConfig()):
            value = cfg.value
            value['track'] = file_name
            value['progress'] = '00:00:00'

        self.business.play_track()


def main() -> int:
    """ main function """

    MicroPlayer()

    return 0


# entry
if __name__ == '__main__':
    _exit(main())
