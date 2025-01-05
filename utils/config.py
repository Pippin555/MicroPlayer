#! python3.13

"""
simple configuration wrapper

usage: create your own configuration based on this meta class:

class MyConfig(Config):
    ''' my config class '''

instantiate the class with the filename of you main file and the default data

value { 'one': 1, 'two': 2 }
with (conf := MyConfig(main=__file__, value=value)):
    pass

in the above construction the configuration is created and written to
C:/users/<current user>/AppData/Roaming/python_data/<main>/<main>.json

because the config class is a singleton, only one instance of the class
will exist in your program

use MyConfig anywhere in  your code:

     my_conf = MyConfig()
     value = my_conf.value
     print(f'one is {value["one"]};)

Note: do not use the following:

with MyConfig(main=__file__, value=value) as conf:
    pass

because that will leave 'conf' being None

depends on: ../utils/singleton.py
"""

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2022-2024 all rights reserved'  # noqa

from os import remove
from os import getenv
from os import mkdir

from os.path import basename
from os.path import splitext
from os.path import isfile
from os.path import join
from os.path import isdir

from typing import Any
from dataclasses import dataclass

# pip install jsons
from jsons import loads
from jsons import dumps

from utils.singleton import Singleton


@dataclass(kw_only=True)
class Config(metaclass=Singleton):
    """ this is the configuration singleton
        usage: see above
    """

    def __init__(self, value: Any = None, main: str = None):
        """ initialize the configuration
        :param value: initial value, if None an empty dictionary will be used
        :param main: the name of the file where the class is first used
                     i.e. main=__file__
        """
        # only assign _value and _config_name the first time this singleton is created
        if not hasattr(self, '_value'):
            if main is None:
                raise ValueError(
                    "The configuration must be initialized with main=__file__")

            self._value = {}
            self._name = Config.get_config_name(main)

            if isfile(self._name):
                with open(file=self._name, mode='r', encoding='utf8') as stream:
                    self._value = loads(stream.read())

            if isinstance(value, dict):
                for key in value:
                    if key not in self._value:
                        self._value[key] = value[key]

    @property
    def value(self):
        """ get the stored configuration """
        return self._value

    # a setter function
    @value.setter
    def value(self, value: Any):
        """ set the value """
        self._value = value

    def save(self) -> None:
        """ save the configuration """
        with open(file=self._name, mode='w', encoding='utf8') as stream:
            stream.write(dumps(self.value))

    @staticmethod
    def clear(main: str) -> None:
        """ remove the configuration file """
        name = Config.get_config_name(main)
        if isfile(name):
            remove(name)

    @staticmethod
    def get_config_name(main: str) -> str:
        """ derive the config name from main """
        name, _ = splitext(basename(main))
        roaming = getenv('AppData')

        python_data = join(roaming, 'python_data')
        if not isdir(python_data):
            mkdir(python_data)

        folder = join(python_data, name)
        if not isdir(folder):
            mkdir(folder)

        return join(folder, f"{name}.json")

    def __enter__(self):
        """ with statement entered """

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ with statement exited """
        self.save()
        # print('saved the config')
