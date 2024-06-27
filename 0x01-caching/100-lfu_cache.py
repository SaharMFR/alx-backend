#!/usr/bin/env python3
""" Defines `LFUCache` class """
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """ Caching system """
    def __init__(self):
        """ Initialize """
        super().__init__()
        self.frequencies = {}

    def put(self, key, item):
        """ Put an item in the cache """
        if key is None or item is None:
            return
        if (len(self.cache_data.keys()) == self.MAX_ITEMS
           and key not in self.cache_data):
            discarded = min(self.frequencies, key=self.frequencies.get)
            self.cache_data.pop(discarded)
            self.frequencies.pop(discarded)
            print("DISCARD:", discarded)
        if key in self.cache_data:
            self.frequencies[key] += 1
        else:
            self.frequencies[key] = 1
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        if key in self.cache_data.keys():
            self.frequencies[key] += 1
            return self.cache_data.get(key)
