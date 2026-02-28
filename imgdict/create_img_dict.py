""" create the image and icon dictionary in code """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

from sys import exit as _exit

from os import curdir

from os import walk

from os.path import join
from os.path import abspath

from PIL import Image

from dict_img_utl import set_image


def create_dict(image_path: str) -> dict:
    """ - """

    image_dict = {}
    for root, _, files in walk(image_path):
        for file in files:
            fullname = abspath(join(root, file))
            image = Image.open(fullname)
            set_image(image_dict=image_dict, key=file.lower(), image=image)

    return image_dict


def stringify_dict(image_dict: dict, filename: str):
    """ ... """

    with open(file=filename, mode='w', encoding='utf8') as stream:
        print('""" image resources """', file=stream)
        print(file=stream)
        print('__author__ = \'auto generated, do not alter\'', file=stream)
        print('__copyright__ = \'© Sihir 2024-2024 all rights reserved\'  # noqa', file=stream)
        print(file=stream)
        print('image_dict2 = {', file=stream)
        for key, value in image_dict.items():
            print(f'        "{key}":"""{value}""", ', file=stream)
        print('}', file=stream)


def main() -> int:
    """ main function """

    image_path = join(curdir, 'icons')
    target_file = abspath(join(curdir, 'imgdict', 'image_dictionary.py'))

    image_dict = create_dict(image_path=image_path)
    stringify_dict(image_dict, filename=target_file)

    return 0


if __name__ == '__main__':
    _exit(main())
