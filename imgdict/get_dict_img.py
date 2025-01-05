#! python3.13
# coding=utf8

""" the GUI for the player """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2024-2024 all rights reserved'  # noqa
__version__ = 'Sihir.entertainment.player.v1.1'  # noqa

from PIL import Image
from PIL.ImageTk import PhotoImage

from imgdict.dict_img_utl import get_image
from imgdict.image_dictionary import image_dict2


def get_img(key: str) -> Image:
    """ return the image from resource dictionary """

    image, _ = get_image(image_dict=image_dict2, key=key)
    return image


def get_ico(key: str, size: tuple = (32, 32)) -> PhotoImage:
    """ return the image as PhotoImage """

    image = get_img(key=key)
    return PhotoImage(image.resize(size))
