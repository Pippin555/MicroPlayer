""" container for mp3 tags """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2025-2025 all rights reserved'  # noqa

from os.path import isfile

from logging import getLogger
from logging import CRITICAL

from eyed3 import AudioFile
from eyed3 import load as _load

from utils.pathtools import has_ext


class Eyed3Wrapper:

    @staticmethod
    def load(file_name: str) -> AudioFile:
        """ checks and loads the file """

        if not isfile(file_name):
            raise FileNotFoundError(file_name)

        if not has_ext(file_name, '.mp3'):
            raise ValueError(f"Unsupported file type: {file_name}")

        logger = getLogger('eyed3')
        original = logger.getEffectiveLevel()
        logger.setLevel(CRITICAL)
        try:
            audio = _load(path=file_name)
            if audio is None:
                raise ValueError(f"File is not a valid MP3: {file_name}")
        finally:
            logger.setLevel(original)

        return audio
