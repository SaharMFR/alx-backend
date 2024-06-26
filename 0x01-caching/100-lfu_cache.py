#!/usr/bin/env python3
""" Defines `LFUCache` class """
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """ Caching system """
    def __init__(self):
        """ Initialize """
        super().__init__()
        self.cache_data = OrderedDict()
        self.frequencies = []

    def reorder_elements(self, mru_key):
        """Reorders the items in this cache based on the most
        recently used item.
        """
        max_positions = []
        mru_freq = 0
        mru_pos = 0
        ins_pos = 0
        for i, key_freq in enumerate(self.frequencies):
            if key_freq[0] == mru_key:
                mru_freq = key_freq[1] + 1
                mru_pos = i
                break
            elif len(max_positions) == 0:
                max_positions.append(i)
            elif key_freq[1] < self.frequencies[max_positions[-1]][1]:
                max_positions.append(i)
        max_positions.reverse()
        for pos in max_positions:
            if self.frequencies[pos][1] > mru_freq:
                break
            ins_pos = pos
        self.frequencies.pop(mru_pos)
        self.frequencies.insert(ins_pos, [mru_key, mru_freq])

    def put(self, key, item):
        """ Put an item in the cache """
        if key is not None or item is not None:
            if key not in self.cache_data:
                if self.MAX_ITEMS < len(self.cache_data) + 1:
                    lfu_key, _ = self.frequencies[-1]
                    self.cache_data.pop(lfu_key)
                    self.frequencies.pop()
                    print("DISCARD:", lfu_key)
                self.cache_data[key] = item
                ins_index = len(self.frequencies)
                for i, key_freq in enumerate(self.frequencies):
                    if key_freq[1] == 0:
                        ins_index = i
                        break
                self.frequencies.insert(ins_index, [key, 0])
            else:
                self.cache_data[key] = item
                self.reorder_elements(key)

    def get(self, key):
        """ Get an item by key """
        if key in self.cache_data:
            self.reorder_elements(key)
        return self.cache_data.get(key, None)
