# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.


from . import base


class MemcacheStorage(base.BaseStorage):
    """A django cache-based storage.

    Attributes:
        cache_name (str): the name of the cache backend to use
        cache: the actual django cache backend
    """

    def __init__(self, client, *args, **kwargs):
        self.client = client
        super(MemcacheStorage, self).__init__(*args, **kwargs)

    def get(self, key, default=None):
        return self.client.get(key, default)

    def set(self, key, value):
        self.client.set(key, value)

    def mget(self, *keys, **kwargs):
        values = self.client.get_many(keys)
        for key in keys:
            yield values[key]

    def mset(self, values):
        self.client.set_many(values)

    def incr(self, key, amount, default=0):
        # Ensure the key exists
        self.client.add(key, default)

        return self.cache.incr(key, amount)
