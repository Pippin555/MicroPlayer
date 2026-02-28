""" tooltip for a widget

gives a Tkinter widget a tooltip as the mouse is above the widget

originally found here:
www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

Modified to include a delay time by Victor Zaccardo, 25 march 2016
"""

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa


import tkinter as tk


class CreateToolTip:
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        """ initialize the class """

        self.wait_time = 500     # milliseconds
        self.wrap_length = 180   # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.ident = None
        self.tool_win = None

    def enter(self, _):
        """ the mouse has entered """

        self.schedule()

    def leave(self, _):
        """ the mouse has left """

        self.unschedule()
        self.hidetip()

    def schedule(self):
        """ schedule show """

        self.unschedule()
        self.ident = self.widget.after(self.wait_time, self.showtip)

    def unschedule(self):
        """ reset the tooltip """

        ident = self.ident
        self.ident = None
        if ident:
            self.widget.after_cancel(ident)

    def showtip(self):
        """ show the tooltip """

        x_pos, y_pos, *_ = self.widget.bbox("insert")
        x_pos += self.widget.winfo_rootx() + 25
        y_pos += self.widget.winfo_rooty() + 20

        # creates a toplevel window
        self.tool_win = tk.Toplevel(self.widget)
        self.tool_win.attributes('-topmost', True)

        # Leaves only the label and removes the app window
        self.tool_win.wm_overrideredirect(True)
        self.tool_win.wm_geometry(f'+{x_pos}+{y_pos}')
        label = tk.Label(self.tool_win,
                         text=self.text,
                         justify='left',
                         background="#ffffff",
                         relief='solid',
                         borderwidth=0,
                         wraplength = self.wrap_length)

        try:
            label.grid(row=0,
                       column=0,
                       padx=2,
                       pady=2,
                       sticky='news')
        except tk.TclError as err:
            print(err)

    def hidetip(self):
        """ hide the tip """

        tool_win = self.tool_win
        self.tool_win= None
        if tool_win:
            tool_win.destroy()
