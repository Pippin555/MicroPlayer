""" Singleton metaclass """

__author__ = 'Sihir'
__copyright__ = '© Sihir 2021-2024 all rights reserved'


class Singleton(type):
    """ metaclass for Singleton """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """ this is run when created """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
