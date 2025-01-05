#! python3.13

""" container for mp3 tags """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2025-2025 all rights reserved'  # noqa

from logging import getLogger
from logging import CRITICAL

from eyed3 import AudioFile
from eyed3 import load as _load


class Eyed3Wrapper:

    @staticmethod
    def load(file_name: str) -> AudioFile:
        """ prevent logging on stderr if not critical """

        logger = getLogger('eyed3')
        original = logger.getEffectiveLevel()
        logger.setLevel(CRITICAL)
        audio = _load(path=file_name)
        logger.setLevel(original)
        return audio