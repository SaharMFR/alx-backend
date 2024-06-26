#!/usr/bin/env python3
""" Defines `LIFOCache` class """
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """ Caching system """
    def __init__(self):
        """ Initislize """
        super().__init__()
        self.__lastKey = None

    def put(self, key, item):
        """ Add an item in the cache """
        if (key not in self.cache_data
                and self.MAX_ITEMS < len(self.cache_data) + 1):
            self.cache_data.pop(self.__lastKey)
            print("DISCARD:", self.__lastKey)
        if key is not None and item is not None:
            self.cache_data[key] = item
            self.__lastKey = key

    def get(self, key):
        """ Get an item by key """
        return self.cache_data.get(key, None)
