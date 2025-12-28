#! python3.13

""" container for mp3 tags """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2021-2024 all rights reserved'  # noqa

from os.path import dirname
from os.path import basename
from os.path import isfile

from typing import Any
from typing import Optional

from io import BytesIO

from PIL import Image

# pip install eyed3
import eyed3
from eyed3.id3 import Genre
from eyed3.core import CountAndTotalTuple

from utils.quick_sort import quicksort
from utils.string_builder import StringBuilder
from utils.eyed3_wrapper import Eyed3Wrapper

from mp3.popularity import get_rating
from mp3.popularity import set_rating

FRONT_COVER = 3


def to_string(date) -> Optional[str]:
    """
    :param date: only return the year
    :return: the date as string
    """
    return None if not date else f"{date.year}"


class Mp3Tags:
    """ storage class for mp3 tags """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, ident: int = -1, **kwargs):
        """ initialize the Mp3Tags class """

        # pylint: disable=invalid-name
        self.id = ident

        if 'dct' in kwargs:
            self.from_dict(kwargs.get('dct', {}))

            if 'folder' in kwargs:
                self.folder = kwargs.get('folder', '')
            return

        self.filename = kwargs.get('filename', '')
        self.folder = kwargs.get('folder', '')
        self.location = kwargs.get('location', '')
        self.title = kwargs.get('title', '')
        self.artist = kwargs.get('artist', '')
        self.album_artist = kwargs.get('album_artist', '')
        self.album = kwargs.get('album', '')
        self.composer = kwargs.get('composer', '')
        self.publisher = kwargs.get('publisher', '')
        self.track_number = Mp3Tags.get_pair(kwargs.get('track_number', ','))
        self.disc_number = Mp3Tags.get_pair(kwargs.get('disc_number', ','))
        self.genre = kwargs.get('genre', '')
        self.release_date = kwargs.get('release_date', '')
        self.original_release_date = kwargs.get('original_release_date', '')
        self.recording_date = kwargs.get('recording_date', '')
        self.comments = kwargs.get('comments', '')
        self.image_count = kwargs.get('image_count', 0)
        self.duration = kwargs.get('duration', self.duration_from_seconds(0))
        self.rating = kwargs.get('rating', 5)
        self.image_width = kwargs.get('image_width', -1)
        self.image_height = kwargs.get('image_height', -1)
        self.image_type = kwargs.get('image_type', -1)
        self.play_count = kwargs.get('play_count', 0)
        self.bit_rate = kwargs.get('bit_rATE', 0)
        self.freq = kwargs.get('freq', 0)
        self.progress = kwargs.get('progress', 0)

    @staticmethod
    def get_pair(value: Optional[str]) -> list:
        """ convert from string to and int pair """
        if ',' in value:
            parts = value.split(',')
            if isinstance(parts[0], int):
                count = int(parts[0])
            else:
                count = 0
            if isinstance(parts[1], int):
                total = int(parts[1])
            else:
                total = 0
            return [count, total]

        return [0, 0]

    @staticmethod
    def set_pair(data: Any) -> str:
        """ convert pair to string """
        if isinstance(data, list):
            return f'{data[0]},{data[1]}'

        return ','

    @staticmethod
    def duration_from_seconds(seconds):
        """ convert seconds to a d:hh:mm:ss format """

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        value = f'{int(days):01d}:{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'
        return value

    @property
    def duration_in_seconds(self) -> int:
        """ convert duration back to seconds """

        parts = self.duration.split(':')
        sec = int(parts[3])
        min = int(parts[2])
        hrs = int(parts[1])
        dys = int(parts[0])
        return sec + 60 * min + 3600 * hrs + 86400 * dys

    @staticmethod
    def to_str(arg):
        """ this attribute is None, a single string or a list of strings """

        if isinstance(arg, str):
            return arg

        if isinstance(arg, list):
            return ', '.join(arg)

        return ''

    @classmethod
    def load(cls, mp3):
        """ create the Mp3Tags from mp3 tags """

        result = Mp3Tags()
        result.from_mp3(mp3)
        return result

    def from_mp3(self, mp3):
        """
        :param mp3: the mp3 input file
        """

        self.title = mp3.tag.title
        self.artist = Mp3Tags.to_str(mp3.tag.artist)
        self.album_artist = Mp3Tags.to_str(mp3.tag.album_artist)
        self.album = mp3.tag.album
        self.composer = mp3.tag.composer
        self.publisher = mp3.tag.publisher
        self.track_number = mp3.tag.track_num
        self.disc_number = mp3.tag.disc_num
        gen = mp3.tag.genre
        self.genre = gen.name if gen else ''
        self.release_date = to_string(mp3.tag.release_date)
        self.original_release_date = to_string(mp3.tag.original_release_date)
        self.recording_date = to_string(mp3.tag.recording_date)
        self.play_count = mp3.tag.play_count
        self.freq = mp3.info.sample_freq
        self.bit_rate = mp3.info.bit_rate_str

        item = mp3.tag.comments.get(description='')
        self.comments = item.text if item else ''

        self.image_width = -1
        self.image_height = -1
        self.image_type = -1

        self.image_count = len(mp3.tag.images)
        if self.image_count == 1:
            for img_data in mp3.tag.images:
                if img_data.picture_type == FRONT_COVER:
                    self.image_type = FRONT_COVER
                    data = img_data.image_data
                    first = Image.open(BytesIO(data))
                    self.image_width = first.width
                    self.image_height = first.height
                    break

        self.duration = Mp3Tags.duration_from_seconds(mp3.info.time_secs)

        self.rating = get_rating(mp3)

    def to_date(self, attrib: str):
        """ date string conversion to date """

        if hasattr(self, attrib):
            data = getattr(self, attrib)
            if data is not None:
                return eyed3.core.Date.parse(data)
        return None

    def patch_mp3(self, mp3):
        """ patch the mp3 tags """

        mp3.tag.title = self.title
        mp3.tag.artist = self.artist
        mp3.tag.album_artist = self.album_artist
        mp3.tag.album = self.album
        mp3.tag.composer = self.composer
        mp3.tag.publisher = self.publisher
        mp3.tag.track_num = Mp3Tags.set_pair(data=self.track_number)
        mp3.tag.disc_num = Mp3Tags.set_pair(data=self.disc_number)
        if self.genre is None or self.genre == 'None':
            self.genre = 'Other'
        mp3.tag.genre = Genre(self.genre)
        mp3.tag.release_date = self.release_date
        mp3.tag.original_release_date = self.original_release_date
        mp3.tag.recording_date = self.to_date('recording_date')
        mp3.tag.comments.set(self.comments, description='')

        try:
            mp3.tag.play_count = self.play_count
        except KeyError:
            pass

        set_rating(mp3, self.rating)

    def from_dict(self, dct):
        """
        :param dct: the dictionary (vertex)
        """

        self.title = dct.get('title', '')
        self.artist = dct.get('artist', '')
        self.album_artist = dct.get('album_artist', '')
        self.album = dct.get('album', '')
        self.composer = dct.get('composer', '')
        self.publisher = dct.get('publisher', '')

        values = Mp3Tags.get_pair(dct.get('track_number', ''))
        self.track_number = CountAndTotalTuple(values[0], values[1])

        values = Mp3Tags.get_pair(dct.get('disc_number', ''))
        self.disc_number = CountAndTotalTuple(values[0], values[1])

        self.genre = dct.get('genre', '')
        self.release_date = dct.get('release_date', '')
        self.original_release_date = dct.get('original_release_date', '')
        self.recording_date = dct.get('recording_date', '')
        self.play_count = dct.get('play_count', 0)
        self.freq = dct.get('sample_freq', 0)
        self.bit_rate = dct.get('bit_rate', 0)
        self.comments = dct.get('comments', '')
        self.image_width = dct.get('image_width', 0)
        self.image_height = dct.get('image_height', 0)
        self.image_type = dct.get('image_type', 0)
        self.image_count = dct.get('image_count', 0)
        self.duration = dct.get('duration', '')
        self.rating = dct.get('rating', 0)

        self.folder = dct.get('folder', '')
        self.filename = dct.get('filename', '')
        self.location = dct.get('location', '')
        self.progress = dct.get('progress', 0.0)

    def __str__(self):
        """ the track information for all attributes """

        builder = StringBuilder()
        dct = self.__dict__
        keys = list(dct.keys())
        quicksort(keys, start=1)

        for key in keys:
            builder.append_line(f"{key:22} {dct[key]}")

        return builder.to_string()

    def compact(self):
        """  the compact track information """

        return f'{self.track_number}\t({self.duration})\t{self.title}'

    @classmethod
    def from_file(cls, file_name: str):
        """ create from file """

        mp3 = Eyed3Wrapper.load(file_name)
        tags = Mp3Tags.load(mp3)
        tags.filename = basename(file_name)
        tags.folder = dirname(file_name)
        return tags

    @staticmethod
    def filter_lame(buf: str) -> str:
        """ Lame CRC errors are not relevant """

        lines = buf.split('\n')
        builder = StringBuilder()

        for line in lines:

            if len(line) == 0:
                continue

            if 'Lame tag CRC check failed' not in line:
                builder.append(line)

        return builder.to_string()
