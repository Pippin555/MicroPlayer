#! python3.13

""" check whether packages have the correct version """

__author__ = 'Sihir'
__copyright__ = "© Sihir 2024-2024 all rights reserved"
__original_code__ = 'ChatGPT 4o'

from sys import exit as _exit

from os.path import splitext
from os.path import isfile

from jsons import dumps
from jsons import loads

from packaging import version

import subprocess


class Configuration:
    """ load or save the configuration """

    def __init__(self):
        """ initialize the class """

        # the default requirements
        self.required_packages = {
            'easyocr': '1.7.1',
            'numpy': '1.26.4',
            'scikit-image': '0.23.2',
            'mkl': '2021.4.0',
            'scipy': '1.13.1',
        }

        path, _ = splitext(__file__)
        conf_name = f'{path}.json'

        if isfile(conf_name):
            with open(file=conf_name, mode='rt', encoding='utf8') as stream:
                self.required_packages = loads(stream.read())
        else:
            with open(file=conf_name, mode='wt', encoding='utf8') as stream:
                stream.write(dumps(self.required_packages))

    def items(self):
        """ return the items of the dictionary """

        return self.required_packages.items()


def check_package_version(package, max_version) -> str:
    """Check one package against the maximum allowed version."""

    try:
        result = subprocess.run(['pip', 'show', package],
                                capture_output=True,
                                text=True,
                                check=True)
        for line in result.stdout.splitlines():
            if line.startswith('Version:'):
                installed_version = line.split(":", 1)[1].strip()
                if version.parse(installed_version) > version.parse(max_version):
                    return (f"Error: {package} version too high. "
                            f"Max allowed: {max_version}, Installed: {installed_version}")
                break
    except subprocess.CalledProcessError:
        return f'Error: {package} is not installed.'
    return ''


def main():
    """ main function """

    messages = []
    for package, version in Configuration().items():
        message = check_package_version(package, version)
        if message:
            messages.append(message)

    if len(messages) == 0:
        print('\nAll required package versions are correct.')

    else:
        print('\nRequirements:')
        for message in messages:
            print(message)


if __name__ == "__main__":
    _exit(main())
