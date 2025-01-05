#! python3.13
# coding=utf8

""" implementation of a Treeview """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

from os.path import isfile
from os.path import join
from os.path import abspath

from typing import Callable

from tkinter.ttk import Style
from tkinter.ttk import Frame
from tkinter.ttk import Treeview
from tkinter import Menu

from functools import partial

from PIL import Image
from PIL.ImageTk import PhotoImage


# pylint: disable=too-many-ancestors
# pylint: disable=too-many-instance-attributes
class TreeviewContainer(Frame):
    """ Treeview helper class """

    def __init__(self, master, **kwargs):
        """ initialize the frame """

        self.master = master
        self.ignore_single_click = False
        self.single_click: Callable = kwargs.get('single_click')
        self.double_click: Callable = kwargs.get('double_click')
        self.context = kwargs.get('context', None)

        # pylint: disable=invalid-name
        self.SortDir = True
        # pylint: enable=invalid-name

        self.image_size = kwargs.get('image_size', (24, 24))
        self.info = {'images': {}}

        Frame.__init__(self, master)

        # width = kwargs.get('width', 100)

        dct = kwargs.get('dct', {})

        height = dct.get('height', 16)
        columns = dct.get('columns', [('first', '', 40)])
        self.data_cols = tuple(header for header, *_ in columns)
        show = dct.get('headings', ('headings', 'tree'))

        self.tree = Treeview(master=master,
                             columns=self.data_cols,
                             height=height,
                             show=show)

        self.tree.grid(row=kwargs.get('row', 0),
                       column=kwargs.get('col', 0),
                       padx=2,
                       pady=2,
                       sticky='news')

        for idx, (_, title, width) in enumerate(columns):
            self.tree.column(f'#{idx}',
                             minwidth=width,
                             width=width + 4,
                             stretch=False)

            self.tree.heading(f'#{idx}',
                              text=title,
                              anchor='w')

        style = Style(master)
        row_height = dct.get('row_height', 4)
        style.configure('Treeview', rowheight=row_height)

        self.tree.bind("<ButtonRelease-1>", self.on_single_click)
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.on_right_click)

    @property
    def control(self):
        """ return the widget """

        return self.tree

    @property
    def selection(self):
        """ return the selected rows """

        return self.tree.selection()

    def populate_row(self, data: list):
        """ populate one row on identifier """

        ident = data[0]
        values = data[1:]
        self.tree.item(item=str(ident), values=values)

    # pylint: disable=too-many-locals
    def populate(self, **kwargs):
        """ populate the tree """

        for row in self.tree.get_children():
            self.tree.delete(row)

        items = kwargs.get('items', [{}])
        for item in items:
            ident = item.get('ident', '')
            index = item.get('index', 'end')
            parent = item.get('parent', '')
            text = item.get('text', '')
            values = item.get('values', [])
            tags = ('folder', ) if parent == '' else ('item', )
            img_name = item.get('img_name', None)

            photo = None
            if img_name is not None:
                images = self.info['images']
                if img_name in images:
                    photo = images[img_name]
                else:
                    image_file = abspath(join('./icons', f'{img_name}.png'))

                    if isfile(image_file):
                        img = Image.open(fp=image_file)
                        img = img.resize(self.image_size)
                        photo = PhotoImage(img)
                        images[img_name] = photo

            row = self.tree.insert(parent=parent,
                                   id=ident,
                                   index=index,
                                   text=text,
                                   values=values,
                                   tags=tags
                                   )
            if parent == '':
                self.tree.item(item=row, open=True)

            if photo is not None:
                self.tree.tag_configure('folder', image=photo)

    def on_single_click(self, event):
        """ single click on tree """

        if self.ignore_single_click:
            self.ignore_single_click = False
            return

        item = self.tree.selection()
        if item is not None and \
                len(item) > 0 and \
                self.single_click is not None:
            who = self.tree.identify("item", event.x, event.y)
            # clicked outside the tree
            if who == '':
                return

            ident = item[0]
            region = self.tree.identify_region(event.x, event.y)
            column = -1  # no cell column
            values = []  # no values
            if region == 'cell':
                col = self.tree.identify_column(event.x)
                column = int(col.lstrip('#')) - 1
                values = self.tree.item(ident)["values"]
            self.single_click(ident, region, column, values)

    def get_ident(self, event):
        """ find the ident """

        return self.tree.identify("item", event.x, event.y)

    def on_double_click(self, event):
        """ double-click on tree """

        item = self.tree.selection()
        if item is not None and self.double_click is not None:
            self.ignore_single_click = True
            ident = self.get_ident(event)
            if ident == '':
                return

            region = self.tree.identify_region(event.x, event.y)  # get click location
            column = 0  # no cell column
            values = []  # no values
            if region == 'cell':
                col = self.tree.identify_column(event.x)
                column = int(col.lstrip('#')) - 1
                values = self.tree.item(ident)["values"]

            self.double_click(ident, region, column - 1, values)

    def on_right_click(self, event):
        """ right click on tree """

        if self.context is not None:
            ident = self.get_ident(event)
            if ident == '':
                return

            menu = Menu(master=self.master,
                        tearoff=False)

            for item in self.context:
                name, cmd = item
                menu.add_command(label=name, command=partial(cmd, ident))

            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
