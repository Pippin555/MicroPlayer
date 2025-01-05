#! python3.13
# coding=utf8

""" the (partial) quicksort algorithm """

__author__ = 'Sihir'  # noqa
__copyright__ = '© Sihir 2023-2024 all rights reserved'  # noqa

# honestly copied from: https://www.geeksforgeeks.org/quicksort-using-random-pivoting/
# see also test_quick_sort.py

from random import randrange
from typing import Optional
from typing import Callable


def quicksort(arr: list, **kwargs) -> None:
    """ in place quick sort an array
    :param arr: the array to sort
    :param start: start index defaults to 0 for None
    :param stop: stop index defaults to len(arr) - 1
    :param reverse: for reverse sorting (high to low) defaults ro 9low to high)
    :param comp: the compare function, defaults to < for None
    :return: None
    """

    start = kwargs.get('start', 0)
    stop = kwargs.get('stop', len(arr) - 1)
    reverse = kwargs.get('reverse', False)
    comp = kwargs.get('comp', None)

    if start < stop:
        pivot_index = _partition_rand(arr,
                                      start,
                                      stop,
                                      reverse=reverse,
                                      comp=comp)
        quicksort(arr,
                  start=start,
                  stop=pivot_index - 1,
                  reverse=reverse,
                  comp=comp)

        quicksort(arr,
                  start=pivot_index + 1,
                  stop=stop,
                  reverse=reverse,
                  comp=comp)


def _partition_rand(arr: list,
                    start: int,
                    stop: int,
                    reverse: bool,
                    comp: Optional[Callable] = None) -> int:
    """ use a random pivot value """

    rand_pivot = randrange(start, stop)
    arr[start], arr[rand_pivot] = arr[rand_pivot], arr[start]

    # perform the partition
    return _partition(arr=arr,
                      start=start,
                      stop=stop,
                      reverse=reverse,
                      comp=comp)


def _partition(arr: list,
               start: int,
               stop: int,
               reverse: bool,
               comp: Optional[Callable] = None) -> int:
    """ do the actual partition """

    pivot = start  # pivot

    # a variable to memorize where the
    # partition in the array starts from.
    idx = start + 1
    for jdx in range(start + 1, stop + 1):

        # use the comparer
        order = arr[jdx] < arr[pivot] if comp is None else comp(jdx, pivot)
        # order = comp(jdx, pivot)

        # the ^ is the xor that reverses the result
        if order ^ reverse:
            arr[idx], arr[jdx] = arr[jdx], arr[idx]
            idx = idx + 1

    arr[pivot], arr[idx - 1] = arr[idx - 1], arr[pivot]
    return idx - 1  # pivot


class IndexedQuicksort:
    """ returns a sorted list of indices, does not rearrange the array """

    def __init__(self):
        """ initialize the class
            needs storage, so class is a better solution
        """
        self.arr = []
        self.idx = []
        self.access: Optional[Callable] = None

    def sort(self, arr: list, **kwargs) -> []:
        """ calls quicksort with a comparer
        :param arr: the array to create an index for
        :return: the indices
        """

        # save the array
        self.arr = arr

        # create the indices
        self.idx = [*range(len(arr))]

        # slicing the array
        start = kwargs.get('start', 0)
        stop = kwargs.get('stop', len(arr) - 1)

        # access function, see below, the lambda here is for self reference
        self.access = kwargs.get('access', lambda x: x)

        # sorting ascending or descending
        reverse = kwargs.get('reverse', False)

        # the compare function, when 'None' the function is __lt__
        comp = kwargs.get('comp', self.comp)

        quicksort(self.idx,
                  start=start,
                  stop=stop,
                  reverse=reverse,
                  comp=comp)

        # return the array of indices
        return self.idx

    def comp(self, left: int, right: int) -> bool:
        """ the actual comparer """

        # sorting the array indirectly

        # get the index to the array
        lid = self.idx[left]
        rid = self.idx[right]

        # get the entry in the array
        lit = self.arr[lid]
        rit = self.arr[rid]

        # access the property in the entry
        # using lambda x: x     for self reference
        # using lambda x: x:[0] for the first element in a tuple or list
        # using lambda x: x.a   for property 'a' in class x
        # and compare
        return self.access(lit) < self.access(rit)


def shuffle(arr: list) -> None:
    """ shuffle whole array inplace, utility function """

    lar = len(arr)
    for iar in range(lar):
        jar = randrange(lar)
        arr[iar], arr[jar] = arr[jar], arr[iar]
