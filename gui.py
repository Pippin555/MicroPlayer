""" the GUI for the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa
__version__ = 'Sihir.entertainment.player.v1.1'  # noqa

from os.path import isfile
from os.path import basename

from tkinter import Tk
from tkinter import Label
from tkinter import PhotoImage

from tkinter.ttk import Style

from typing import Optional
from typing import Callable

from ctypes import windll

from business import PyPlayerBusiness
from player_config import MicroPlayerConfig

from utils.tools import to_dhms
from utils.tools import from_dhms
from utils.tools import has_ext

from gui_buttons import GuiButtons

from mp3.mp3tags import Mp3Tags

from imgdict.get_dict_img import get_ico


class PyPlayerGui:
    """ the GUI for the player """

    def __init__(self,
                 business: PyPlayerBusiness,
                 track_selected: Callable):
        """ initialize the class"""

        self.business = business
        self._buttons = None
        self._track_selected = track_selected
        self.file = None
        self._closed = False
        self._transition = False

        self._master = root = Tk()

        icon = PyPlayerGui.set_icon(root=root)

        root.protocol("WM_DELETE_WINDOW", self._quit)

        selected = 0
        self.value = MicroPlayerConfig().value
        self.controls = {
            'root': root,
            'is_paused': False,
            'duration': 0,
            'selected': selected,
            'offset': 0,
            'position': self.value.get('position', (200, 100)),
            'icon': icon,
        }

        # interface to button functions
        self.buttons = {}
        self._load_icons()

    @property
    def master(self):
        """ ... """

        return self._master

    @staticmethod
    def set_icon(root: Tk) -> Optional[PhotoImage]:
        """ set window icon and taskbar icon """

        root.title('MicroPlayer')
        icon = get_ico(key='player.ico', size=(20, 20))
        try:
            root.iconphoto(False,
                           icon,
                           icon)  # noqa _PhotoImageLike can't be referenced
            # copy to the taskbar icon
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(__version__)
            return icon

        # pylint: disable=broad-exception-caught
        except Exception as exc:
            print(exc)

        return None

    def start(self, autostart: bool):
        """ start the player """

        if autostart:
            self.business.start()

    @property
    def root(self):
        """ return the root of the Gui """

        return self.controls['root']

    def create_gui(self):
        """ create the GUI """

        root = self.controls['root']

        root.resizable(width=False, height=False)

        buttons = GuiButtons(owner=self,
                             business=self.business,
                             track_selected=self._track_selected)

        buttons.create_buttons()
        self._buttons = buttons

        value = MicroPlayerConfig().value
        track = value.get('track', None)

        if track is None:
            message = 'Busy...'

        elif not has_ext(track, '.mp3'):
            message = f"can't handle {basename(track)}"
            track = None

        elif not isfile(track):
            message = f'track not found: {track}'
            track = None

        else:
            mp3 = Mp3Tags.from_file(track)

            title = mp3.title
            composer = mp3.composer
            message = f'{composer} - {title}'

        buttons.set_result(message)

        #if track is not None:
            # pass this function to business layer
        self.business.set_play_track(self.get_track)

    def run(self):
        """ run the GUI """

        self.controls['root'].mainloop()

    def _load_icons(self):
        """ get the icon by name and save the image """

        icons = {}
        for name in ['stop',
                     'play',
                     'pause',
                     'repeat',
                     'speaker_up',
                     'speaker_down',
                     'speaker_off',
                     'speaker_on',
                     'mp3',
                     'lyr_off',
                     'lyr_on']:

            icon = get_ico(key=name + '.ico', size=(20, 20))
            icons[name] = icon

        self.controls['icons'] = icons

    def _quit(self):
        """ quit the program """

        self._closed = True

        # save the last progress
        with (conf := MicroPlayerConfig()):
            assert conf.value

        # stop the mixer
        self._buttons.stop()
        self.controls['root'].destroy()

    def random_track(self):
        """ select a random track,
            this is rather slow when the program just started running
            so the call is done "in the background"
        """

        self.controls['root'].after(50, self.get_track)

    def _get_icon(self, name: str):
        """ get the icon """

        return self.controls['icons'][name]

    def _set_button(self, button_name: str, icon_name: str):
        """ set the button image """

        button = self.buttons[button_name]
        button.config(image=self._get_icon(icon_name))

    def get_track(self) -> bool:
        """ load the track """

        self._transition = True

        value = MicroPlayerConfig().value

        result = value.get('track', None)
        if result is None:
            return False

        if not isfile(result):
            return False

        if 'progress' not in value:
            return False

        # read the progress from the config file
        progress = value.get('progress', 0.0)

        selected = 0
        duration = 0

        # to do: move to the business layer
        try:
            self.file = Mp3Tags.from_file(result)
            mp3 = self.file
            duration = mp3.duration
            title = mp3.title
            composer = mp3.composer
            artist = mp3.artist
            who = composer if composer is not None else artist
            selected = 0

            self.set_result(text=f'{title} - {who}')

        except ValueError as vex:
            self.set_result(text=str(vex.args[0]))
            return False

        except Exception as exc:
            self.set_result(text=exc.message)
            return False

        self.controls['selected'] = selected
        self.controls['duration'] = duration
        self._buttons.load(result, duration, progress)
        self._set_button(button_name='play', icon_name='pause')

        return True

    def get_progress(self):
        """ at how many seconds is the player """

        # system is shutting down
        if self._closed:
            # print('shutting down')
            return 0

        # print('pyPlayer.get progress')

        pos = self._buttons.get_progress()
        self._show_progress(pos)

        if pos is not None:
            self._save_progress(pos)

        return pos

    def _show_progress(self, progress: Optional[float]):
        """ show the progress on the progress label """

        duration = self.controls['duration']
        if progress is None:
            text = ''
        else:
            text = f'{to_dhms(int(progress))} of {duration}'

        value = MicroPlayerConfig().value
        if self._buttons.get_busy():
            value['progress'] = progress
            # print(progress)

        progressbar: Style = self.controls['progress_style']
        progressbar.configure('LabeledProgressbar', text=text)

        value = 0 if duration is None or progress is None or duration == 0 \
            else 100.0 * progress / from_dhms(str(duration))

        self.controls['pbar']['value'] = int(value)  # noqa for 'pbar'

    def _save_progress(self, progress: int):
        """ save the progress in the DB """

        selected = self.controls['selected']
        self.business.save_progress(selected, progress)

    def set_result(self, text: str):
        """ set the result label text """

        result_label: Label = self.controls['result_label']
        result_label.config(text=text)

    def get_busy(self) -> int:
        """
        returns:
            0 when stopped
            1 when playing
            2 when paused
        """

        return self._buttons.get_busy()

    def set_sender(self, sender: str):
        """ update the caption """

        self.controls['root'].title(f'MicroPlayer {sender}')
