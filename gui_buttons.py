#! python3.13

""" the GUI for the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa
__version__ = 'Sihir.entertainment.player.v1.0'  # noqa

from os.path import dirname
from os.path import isfile

from tkinter import Frame
from tkinter import Button
from tkinter import Label

from tkinter.filedialog import askopenfilename

from tkinter.ttk import Progressbar
from tkinter.ttk import Style

from typing import Callable

from pymixer import PyMixer

from utils.py_input import volume_up
from utils.py_input import volume_down
from utils.string_builder import StringBuilder

from business import PyPlayerBusiness

from widgets.hms_container import HmsContainer
from player_config import MicroPlayerConfig

from popup_helper import PopupHelper


class GuiButtons:
    """ the buttons on the GUI """

    def __init__(self,
                 owner,
                 business: PyPlayerBusiness,
                 track_selected: Callable):
        """ initialize the GuiButtons """

        self.master = owner
        self.controls = owner.controls
        self._buttons = owner.buttons
        self._business = business
        self._business.result_callback = self.set_result
        self.track_selected = track_selected
        self.track = None
        self.duration = 0
        self._hms = None

        self._mixer = PyMixer(finished=self.finished)
        business.mixer = self._mixer

    def _create_button(self, name: str, column: int, func: Callable, frame: Frame):
        """ append a button"""

        icon = self._get_icon(name)
        self._buttons[name] = Button(master=frame,
                                     image=icon,
                                     command=func)

        self._buttons[name].grid(row=0,
                                 column=column,
                                 ipadx=0,
                                 ipady=0,
                                 padx=1,
                                 pady=2,
                                 sticky='w')

    def create_buttons(self):
        """ Buttons in the GUI """

        root = self.controls['root']
        button_frame = Frame(master=root)
        row_zero = Frame(button_frame)
        row_zero.grid(row=0,
                      column=0,
                      columnspan=3,
                      padx=(4, 0),
                      pady=(1, 1),
                      sticky='w')

        buttons = [
            ('mp3', self._open),
            ('play', self._play),
            ('stop', self.stop),
            ('repeat', self._repeat),
            ('speaker_up', self._speaker_up),
            ('speaker_down', self._speaker_down)
        ]

        for column, (name, func) in enumerate(buttons):
            self._create_button(name=name,
                                column=column,
                                func=func,
                                frame=row_zero)

        style = Style(root)
        # add the label to the progressbar style
        style.layout("LabeledProgressbar",
                     [('LabeledProgressbar.trough',
                       {'children': [('LabeledProgressbar.pbar',
                                      {'side': 'left',
                                       'sticky': 'ns'}),
                                     ('LabeledProgressbar.label',  # label inside the bar
                                      {'sticky': ''})],
                        'sticky': 'news'
                        }
                       )
                      ])

        style.configure("LabeledProgressbar",
                        background='cyan')

        self.controls['progress_style'] = style

        pbar = Progressbar(master=row_zero,
                           orient='horizontal',
                           length=284,
                           mode='determinate',
                           style="LabeledProgressbar")
        pbar.grid(row=0,
                  column=len(self._buttons),
                  padx=(2, 4),
                  pady=(3, 1))

        pbar.bind('<Button-1>', self._change_progress)
        pbar.bind('<Button-3>', self._context)

        self.controls['pbar'] = pbar

        row_one = Frame(button_frame)
        row_one.grid(row=1,
                     column=0,
                     padx=2,
                     pady=(0, 1),
                     sticky='ew')
        row_one.rowconfigure(1, weight=1)

        support_lyrics = True

        if support_lyrics:
            row_one.grid_columnconfigure(index=0, weight=0)
            row_one.grid_columnconfigure(index=1, weight=1)

            lyr = Label(master=row_one,
                        text='    ',
                        borderwidth=1,
                        image=self._get_icon('lyr_off'),
                        relief = 'raised')

            lyr.grid(row=1,
                     column=0,
                     padx=1,
                     pady=(0,0),
                     sticky='news')

            lyr.bind('<Button-1>', self._show_lyrics)
            col = 1,
        else:
            row_one.grid_columnconfigure(index=0, weight=1)
            col = 0

        ctrl1 = Label(master=row_one,
                      text='result',
                      borderwidth=1,
                      justify='left',
                      relief='raised',
                      anchor='w')

        ctrl1.grid(row=1,
                   column=col,
                   padx=(1, 4),
                   pady=0,
                   sticky='we')

        self.controls['result_label'] = ctrl1

        button_frame.grid(row=0,
                          column=0,
                          sticky='ew')

        button_frame.grid_columnconfigure(0, weight=1)

    def _change_progress(self, event):
        """ progress was clicked """

        pbar = event.widget
        width = pbar.winfo_width()
        pos = event.x / float(width)
        self._mixer.change_progress(pos)
        self.get_progress()

    def _speaker_up(self):
        """ higher volume """

        assert self
        volume_up()

    def _speaker_down(self):
        """ lower volume """

        assert self
        volume_down()

    def _get_icon(self, name: str):
        """ get the icon """

        return self.controls['icons'][name]

    def _set_button(self, button_name: str, icon_name: str):
        """ set the button image """

        button = self._buttons[button_name]
        button.config(image=self._get_icon(icon_name))

    def finished(self):
        """ player finished """

        self._mixer.unload()

    def _open(self):
        """ open a file """

        with (config := MicroPlayerConfig()):
            value = config.value

            cwd = value.get('folder', 'C:\\')

            file_name = askopenfilename(defaultextension='.m3u',
                                        initialdir=cwd,
                                        initialfile='*.mp3',
                                        filetypes=[('Play list', '*.m3u')])

            if file_name and self.track_selected:
                if isfile(file_name):
                    self.track_selected(file_name=file_name)
                    value['folder'] = dirname(file_name)

    def load(self, track: str, duration: int, progress: int):
        """ load and play a track """

        self.track = track
        self.duration = duration
        self._mixer.load(track, duration, progress)

    def get_progress(self):
        """ at how many seconds is the player """

        return self._mixer.get_progress()

    def _play(self):
        """ play or pause """

        icon_name = self._mixer.play()
        self._set_button(button_name='play', icon_name=icon_name)

    def stop(self):
        """ stop playing """

        self._mixer.stop()

    def _repeat(self):
        """ repeat the track """

        if self.track:
            self._mixer.load(track=self.track, duration=self.duration, progress=0)

    def get_busy(self) -> int:
        """
        returns:
            0 when stopped
            1 when playing
            2 when paused
        """

        return self._mixer.busy

    def _context(self, event):
        """ right click called """

        if self._hms:
            self._hms.close()
            self._hms = None

        root = self.controls['root']

        x_pos = event.x_root
        y_pos = event.y_root

        progress = self.get_progress()
        if progress is None:
            return

        second = progress % 60
        minute = int(progress / 60)
        hour = int(minute / 60)
        minute = minute % 60

        self._hms = HmsContainer(
            master=root,
            x_pos=x_pos,
            y_pos=y_pos,
            value=(hour, minute, second),
            callback=self._hms_ok)

    def _hms_ok(self, value: tuple):
        """ change the progress """

        self._mixer.reposition(value)

    def set_result(self, text: str):
        """ set the result label text """

        self.controls['result_label'].config(text=text)

    def _show_lyrics(self, _):
        """ ... """

        builder = StringBuilder()
        aln = builder.append_line

        aln("this is the display for the lyrics")
        aln('when the lyrics are available')

        self._business.popup_helper.do_popup(
            builder=builder,
            root=self.master.root,
            mode='list',
            title='Lyrics')
