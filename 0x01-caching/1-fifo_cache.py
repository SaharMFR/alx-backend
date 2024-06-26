#!/usr/bin/env python3
""" Defines `FIFOCache` class """
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """ Caching system """
    def __init__(self):
        """ Initialize """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            self.cache_data[key] = item
        if self.MAX_ITEMS < len(self.cache_data):
            first_key = list(self.cache_data.keys())[0]
            self.cache_data.pop(first_key)
            print("DISCARD:", first_key)

    def get(self, key):
        """ Get an item by key """
        return self.cache_data.get(key, None)
