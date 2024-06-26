#!/usr/bin/env python3
""" Defines `MRUCache` class """
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """ Caching system """
    def __init__(self):
        super().__init__()
        self.__mru = None

    def put(self, key, item):
        """ Add an item in the cache """
        if (key not in self.cache_data
                and self.MAX_ITEMS < len(self.cache_data) + 1):
            self.cache_data.pop(self.__mru)
            print("DISCARD:", self.__mru)
        if key is not None and item is not None:
            self.cache_data[key] = item
            self.__mru = key

    def get(self, key):
        """ Get an item by key """
        if key is not None and key in self.cache_data:
            self.__mru = key
            return self.cache_data.get(key)
