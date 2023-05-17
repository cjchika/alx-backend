#!/usr/bin/env python3
"""Module containing LFUCache class class"""

from datetime import datetime
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class

    Args:
        BaseCaching ([type]): [Parent class]
    """
    def __init__(self):
        """Init method
        """
        super().__init__()
        self.lru_dict = {}
        self.lfu_dict = {}

    def put(self, key, item):
        """put function

        Args:
            key ([type]): [key argument]
            item ([type]): [item argument]
        """
        if key is None or item is None:
            pass
        else:
            if len(self.cache_data) < BaseCaching.MAX_ITEMS or \
                                    key in self.cache_data.keys():
                if key in self.lfu_dict.keys():
                    self.lfu_dict[key] += 1
                else:
                    self.lfu_dict[key] = 1
                self.lru_dict[key] = datetime.now()
                self.cache_data[key] = item

            else:
                min_value = min(list(self.lfu_dict.values()))
                my_list = []

                for my_key, my_value in self.lfu_dict.items():
                    if my_value == min_value:
                        my_list.append(my_key)

                index = my_list[0]
                tmp = self.lru_dict[my_list[0]]
                for new_key, new_value in self.lru_dict.items():
                    if new_key in my_list and new_value < tmp:
                        tmp = new_value
                        index = new_key
                print("DISCARD: {}".format(index))
                self.lru_dict.pop(index)
                self.lfu_dict.pop(index)
                self.cache_data.pop(index)

                if key in self.lfu_dict.keys():
                    self.lfu_dict[key] += 1
                else:
                    self.lfu_dict[key] = 1
                self.lru_dict[key] = datetime.now()
                self.cache_data[key] = item

    def get(self, key):
        """Module to get a value of the dict

        Args:
            key ([type]): [key argument]

        Returns:
            [type]: [Value]
        """
        if key is None:
            return None
        try:
            value = self.cache_data[key]
            self.lru_dict[key] = datetime.now()
            self.lfu_dict[key] += 1
        except KeyError:
            return None
        return value