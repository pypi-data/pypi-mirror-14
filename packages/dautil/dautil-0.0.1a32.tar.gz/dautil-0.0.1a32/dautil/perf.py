import timeit
import numpy as np
from time import time as now
import sys


def time_once(code, n=1):
    ''' Measures execution time of code (best of 3).

    :param code: Code string or callable.
    :param n: Number of times to repeat execution (n x 3).

    :returns: The best execution time.
    '''
    times = min(timeit.Timer(code).repeat(3, n))

    return np.array(times)/n


class LRUCache():
    ''' Given a function and LRU caching implementation,
        caches the results of the function.

        :ivar impl: LRU cache implementation, for instance \
            `functools.lru_cache`.
        :ivar func: The function to cache.
        :ivar maxsize: The size of the cache.
        :ivar typed: Determines whether a distinction is \
            made between arguments of different types.
        :ivar cached: The cached function.

        >>> from dautil import perf
        >>> from functools import lru_cache
        >>> cache = perf.LRUCache(lru_cache, lambda x: x)
        >>> cache.cache()
        >>> cache.cached(1)
        1
        >>> cache.cached(1)
        1
        >>> cache.hits_miss()
        1.0
    '''
    def __init__(self, impl, func,
                 maxsize=128, typed=False):
        '''

        :param impl: LRU cache implementation, for instance \
            functools.lru_cache.
        :param func: The function to cache.
        :param maxsize: The size of the cache.
        :param typed: Determines whether a distinction is \
            made between arguments of different types.
        '''
        self.impl = impl
        self.func = func
        self.maxsize = maxsize
        self.typed = typed
        self.cached = None
        self.info = None

    def cache(self):
        ''' Caches the function.  '''
        self.cached = self.impl(self.maxsize,
                                self.typed)(self.func)

    def clear(self):
        ''' Clears the cache. '''
        if self.cached:
            self.cached.cache_clear()
            self.info = None

    def get_info(self):
        ''' Gets cache info. '''
        if self.cached:
            self.info = self.cached.cache_info()

    def hits_miss(self):
        ''' Calculates hits/miss ratio.
            In a muti-threaded environment, the calculation is approximate.

        :returns: The hits/miss ratio.
        '''
        if self.info is None:
            self.get_info()

        if self.info.misses == 0:
            return None

        return self.info.hits/self.info.misses


class StopWatch():
    ''' A simple stopwatch, which has a context manager.

    :ivar elapsed: Elapsed time in seconds.

    >>> from dautil import perf
    >>> with perf.StopWatch() as sw:
    ...     pass
    ...
    >>> sw.elapsed
    7.867813110351562e-06
    '''
    def __enter__(self):
        self.begin = now()
        self.elapsed = 0
        return self

    def __exit__(self, *args):
        self.elapsed = now() - self.begin


class CountMinSketch():
    ''' CountMin sketch implementation.

    :ivar depth: Depth of the CountMin sketch table.
    :ivar width: Width of the CountMin sketch table.
    :ivar table: The CountMin sketch table.
    '''
    def __init__(self, depth=5, width=20, seed=28):
        self.depth = depth
        self.width = width
        np.random.seed(seed)
        self.table = np.zeros((depth, width))
        self.hashes = np.random.random_integers(0, sys.maxsize - 1, depth)
        self.PRIME_MODULUS = (1 << 31) - 1

    def hash(self, item, i):
        ''' Calculates the hash for a given item.

        :param item: An item.
        :param i: The index for which to compute the hash.

        :returns: The hash for the item.
        '''
        hval = self.hashes[i] * item
        hval += hval >> 32
        hval &= self.PRIME_MODULUS

        return int(hval) % self.width

    def add(self, item):
        ''' Adds an item.

        :param item: An item.
        '''
        for i in range(self.depth):
            self.table[i][self.hash(item, i)] += 1

    def estimate_count(self, item):
        ''' Estimates the count for an item.

        :param item: An item.

        :returns: The estimated count.
        '''
        res = sys.maxsize

        for i in range(self.depth):
            res = min(res, self.table[i][self.hash(item, i)])

        return res
