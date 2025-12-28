""" the GUI for the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2025 all rights reserved'  # noqa

from sys import exit as _exit
from sys import argv

from time import sleep

from os.path import isfile

from utils.single_instance import single_instance
from utils.string_builder import StringBuilder

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
        self.connection = None

        port = 5001
        with (cfg := MicroPlayerConfig(main=__file__, value=value)):
            value = cfg.value
            if 'port' not in value:
                value['port'] = str(port)

            track = value.get('track', None)
            if track is None or not isfile(track):
                value['track'] = "C:\\bin\\Boenda Moelia II.mp3"

            it_arg = iter(argv[1:])
            for arg in it_arg:
                match arg:
                    case '-p':
                        str_port = next(it_arg, str(port))
                        value['port'] = str_port
                        port = int(str_port)

                    case _:
                        value['track'] = next(it_arg, None)

        self.business = PyPlayerBusiness()
        self.gui = PyPlayerGui(business=self.business,
                               track_selected=self.select_track)

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

        self.updater()

        self.gui.run()

        if self.connection:
            self.connection.close()

        sleep(2)

    def updater(self):
        """ ... """

        print('updater: get_progress')
        self.gui.get_progress()
        print('updater: connection.update()')
        self.connection.update()
        self.gui.master.after(2000, self.updater)

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

        if not isfile(file_name):
            builder = StringBuilder(
                f'File not found:\n{file_name}')

            self.business.do_popup(
                root=self.gui.root,
                builder=builder,
                seconds=5)

            return

        with (cfg := MicroPlayerConfig()):
            value = cfg.value
            value['track'] = file_name
            value['progress'] = '00:00:00'

        self.business.play_track()


def main() -> int:
    """ main function """

    instance, pgm_name = single_instance()
    if instance:
        MicroPlayer()
    else:
        print(f'Only one instance of {pgm_name} can be started')
        return 1

    return 0


# entry
if __name__ == '__main__':
    _exit(main())
