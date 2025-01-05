#! python3.13
# coding=utf8

""" utilities for image resources, use Pillow Image for conversion """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2024-2024 all rights reserved'  # noqa

from os.path import splitext

from base64 import decodebytes as decode_b64
from base64 import encodebytes as encode_b64

from io import BytesIO

from typing import Optional

from PIL import Image


def get_fmt(file: str) -> Optional[str]:
    """ image format based on the file extension  """

    _, ext = splitext(file)

    match ext.lower():
        case '.ico':
            return 'ICO'

        case '.png':
            return 'PNG'

        case ('.jpg' | '.jpeg'):
            return 'JPEG'

    return None


def b64_encode(value: bytes) -> str:
    """ encode using base64
    :param value: the byte array to be encoded
    """

    return encode_b64(value).decode('utf8')


def b64_decode(value: str) -> bytes:
    """ decode using base64
    :param value: the string to be decoded
    """

    return decode_b64(value.encode('utf8'))


def get_image(image_dict: dict, key: str) -> (Image, str):
    """ convert the b64 image back to Pillow.Image """

    value = image_dict.get(key, '')
    if value == '':
        return None, None

    data = b64_decode(value)
    io = BytesIO()
    io.write(data)
    return Image.open(io), get_fmt(key)


def set_image(image_dict: dict, key: str, image: Image):
    """ save an image in b64 format in a dictionary using Pillow.Image """

    buff = BytesIO()
    fmt = get_fmt(key)
    image.save(buff, format=fmt)
    barr = buff.getbuffer()
    data = barr.tobytes()
    encoded = b64_encode(data)
    image_dict[key] = encoded
