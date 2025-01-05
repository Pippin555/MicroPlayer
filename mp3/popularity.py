#! python3.13

""" popularity module interface """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2021-2024 all rights reserved'

import eyed3
import eyed3.id3


# pylint: disable=broad-except
def get_rating(mp3) -> int:
    """ get the rating from the popularity frame """
    acc = eyed3.id3.tag.PopularitiesAccessor(mp3.tag.frame_set)
    # acc.set(email=b'', rating=191,  play_count=0)
    data = acc.get(email=b'')
    value = data.rating if data else 196

    # 224–255 = 5 stars when READ with Windows Explorer, writes 255
    # 160–223 = 4 stars when READ with Windows Explorer, writes 196
    # 096-159 = 3 stars when READ with Windows Explorer, writes 128
    # 032-095 = 2 stars when READ with Windows Explorer, writes 64
    # 001-031 = 1 star when READ with Windows Explorer, writes 1

    if value in range(224, 256):
        rating = 5
    elif value in range(160, 224):
        rating = 4
    elif value in range(96, 160):
        rating = 3
    elif value in range(32, 96):
        rating = 2
    elif value in range(1, 32):
        rating = 1
    else:
        rating = 0
    return rating


def set_rating(mp3, rating) -> int:
    """ set the rating in the popularity frame """
    if rating == 5:
        value = 255
    elif rating == 4:
        value = 196
    elif rating == 3:
        value = 128
    elif rating == 2:
        value = 64
    elif rating == 1:
        value = 1
    else:
        value = 0

    try:
        acc = eyed3.id3.tag.PopularitiesAccessor(mp3.tag.frame_set)
        acc.set(email=b'', rating=value, play_count=0)
    except Exception as exc:
        print(str(exc))
        raise

    return 0
