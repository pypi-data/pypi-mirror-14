""" This module contains utilities related to collections."""

from dautil import log_api
from itertools import chain
from itertools import groupby
import collections


def chunk(alist, size):
    """Yields equal sized chunks from a list.

    :param alist: List-like sequence.
    :param size: Size of the chunk.

    >>> from dautil import collect
    >>> collect.chunk(list(range(7)), 3)
    <generator object chunk at 0x1006a7480>
    >>> next(collect.chunk(list(range(7)), 3))
    [0, 1, 2]
    """
    for i in range(0, len(alist), int(size)):
        yield alist[i:i + size]


def longest_streak(arr, val):
    ''' Counts the number of elements in the longest streak \
        for a given value.

    :param arr: A 1-d list.
    :param val: The value to search for.

    :returns: The count of the longest sequence.

    >>> from dautil import collect
    >>> collect.longest_streak([0, 1, 1, 0, 1, 1, 1], 1)
    3
    '''
    max_count = 0

    for k, g in groupby(arr, lambda x: x == val):
        if not k:
            continue

        count = sum(1 for i in g)

        if count > max_count:
            max_count = count

    return max_count


def sort_dict_by_keys(adict):
    """ Sorts a dictionary by keys.

    :param adict: A dictionary.

    :returns: An `OrderedDict` sorted by keys.

    >>> from dautil import collect
    >>> food = {'spam': 42, 'eggs': 28}
    >>> collect.sort_dict_by_keys(food)
    OrderedDict([('eggs', 28), ('spam', 42)])
    """
    return collections.OrderedDict(sorted(adict.items(), key=lambda t: t[0]))


def dict_from_keys(adict, keys):
    """ Selects a subset of a dictionary with a list of keys.

    :param adict: A dictionary.
    :param keys: A list of keys.

    :returns: A subset of the input dictionary.

    >>> from dautil import collect
    >>> adict = {'a.latex': 1, 'b.latex': 2, 'c': 3}
    >>> collect.dict_from_keys(adict, ['b.latex', 'a.latex'])
    {'a.latex': 1, 'b.latex': 2}
    """
    return {k: adict[k] for k in keys}


def filter_list(func, alist):
    """ Filters a list using a function.

    :param func: A function used for filtering.
    :param alist: The list to filter.

    :returns: The filtered list.

    >>> from dautil import collect
    >>> alist = ['a', 'a.color', 'color.b']
    >>> collect.filter_list(lambda x: x.endswith('color'), alist)
    ['a.color']
    """
    return [a for a in alist if func(a)]


def filter_dict_keys(func, adict):
    """ Filters the keys of a dictionary.

    :param func: A function used to filter the keys.
    :param adict: A dictionary.

    :returns: A list of keys selected by the filter.

    >>> from dautil import collect
    >>> adict = {'a.latex': 1, 'b.latex': 2, 'c': 3}
    >>> collect.filter_dict_keys(lambda x: x.endswith('.latex'), adict)
    ['a.latex', 'b.latex']
    """
    logger = log_api.env_logger()
    logger.debug('adict {}'.format(adict))

    return [k for k in adict.keys() if func(k)]


def dict_updates(old, new):
    """ This function reports updates to a dict.

    :param old: A dictionary to compare against.
    :param new: A dictionary with potential changes.

    :returns: A dictionary with the updates if any.
    """
    updates = {}

    for k in set(new.keys()).intersection(set(old.keys())):
        if old[k] != new[k]:
            updates.update({k: new[k]})

    return updates


def is_rectangular(alist):
    """ Checks whether a list is rectangular.

    :param alist: A list or similar data structure.

    :returns: True if the argument is rectangular.

    >>> from dautil import collect
    >>> collect.is_rectangular([[2, 1], [3]])
    False
    >>> collect.is_rectangular([[2, 1], [3, 4]])
    True
    """
    lengths = {len(i) for i in alist}

    return len(lengths) == 1


def isiterable(tocheck):
    """ Checking for an iterable argument using a
    somewhat modified definition ie strings and dicts
    are considered not iterable.

    :param tocheck: The data structure to check.

    :returns: True if iterable
    """
    return not isinstance(tocheck, str) and\
        not isinstance(tocheck, dict) and\
        isinstance(tocheck, collections.Iterable)


def flatten(iterable):
    """ Flattens an iterable, where strings and dicts
    are not considered iterable.

    :param iterable: The iterable to flatten.

    :returns: The iterable flattened as a flat list.

    >>> from dautil import collect
    >>> collect.flatten([[1, 2]])
    [1, 2]
    """
    logger = log_api.env_logger()
    logger.debug('Iterable {}'.format(iterable))
    assert isiterable(iterable), 'Not iterable {}'.format(iterable)
    flat = iterable

    if isiterable(iterable[0]):
        flat = [i for i in chain.from_iterable(iterable)]

    return flat


def grid_list(arr):
    ''' Creates a 2D cartesian product grid from an array:

    >>> from dautil import collect
    >>>  arr = list(range(2))
    >>> arr
    [0, 1]
    >>> collect.grid_list(arr)
    [[(0, 0), (0, 1)], [(1, 0), (1, 1)]]


    :param arr: A 1-d array-like list.

    :returns: A 2-d list containing tuples as elements.
    '''
    dim = len(arr)
    grid = GridList(dim, dim, 0).grid

    for i in range(dim):
        for j in range(dim):
            grid[i][j] = (arr[i], arr[j])

    return grid


class GridList():
    """ A two-dimensional rectangular list.

    :ivar nrows: The number of rows in the grid.
    :ivar ncols: The number of columns in the grid.
    :ivar val: The initial value of cells in the grid.
    :ivar logger: The logger of the class.
    """
    def __init__(self, nrows, ncols, val):
        self.nrows = nrows
        self.ncols = ncols
        self.grid = [ncols * [val] for i in range(nrows)]
        self.logger = log_api.conf_logger('collect.GridList')

    def dim_equal(self, other):
        """ Checks whether the dimensions of the current GridList
        and another rectangular list are equal.

        :param other: Another rectangular list.

        :returns: True if both data structures have the same dimensions.
        """
        return len(other) == self.nrows and len(other[0]) == self.ncols

    def copy(self, other):
        """ Copies the contents of another list
        into the current GridList.

        :param other: Another list.
        """
        flat_grid = flatten(self.grid)
        flat_other = chain.from_iterable(other)

        for i, value in enumerate(flat_other):
            flat_grid[i] = value

        item = iter(flat_grid)

        for i in range(self.nrows):
            for j in range(self.ncols):
                self.grid[i][j] = next(item)

    def fill(self, other):
        """ Fills the current GridList with the contents
        of another GridList as much as possible, unless
        there is a chance of overflow.

        :param: other: Another list.
        """
        # If edited may become jagged
        if is_rectangular(other):
            if self.dim_equal(other):
                self.grid = other

                return

            ocells = len(other) * len(other[0])
            ncells = self.nrows * self.ncols

            if ocells > ncells:
                # might lose info
                self.logger.warning('Filling {0} with {1}'.format(ncells,
                                                                  ocells))
            else:
                self.copy(other)

    def update(self, row, col, change):
        """ Updates a specific grid cell.

        :param row: The row number of the cell.
        :param col: The column number of the cell.
        :param change: The content with which to update\
            the cell. If the cell is a dict and the update value\
            too then the original dict will be updated.
        """
        cell = self.grid[row][col]

        if isinstance(cell, dict):
            if len(cell.keys()) == 0:
                cell = change
            else:
                (cell).update(change)

        self.grid[row][col] = cell


class IdDict():
    ''' Dictionary for items identified by integers.

    :ivar curr: The current position.
    :ivar items: The dictionary.
    '''
    def __init__(self, items={}):
        self.curr = 0
        self.items = items

    def add_or_get(self, item):
        ''' Adds or gets the id of an item.

        :param item: The item.

        :returns: The id.
        '''
        if self.items.get(item, None) is None:
            self.curr += 1
            self.items[item] = self.curr

        return self.items[item]

    def get_id(self, item):
        ''' Gets the id of an item.

        :param item: The item.

        :returns: The id.
        '''
        return self.items[item]
