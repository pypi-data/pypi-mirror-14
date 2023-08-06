from collections import OrderedDict, MutableMapping


class LRUCache(MutableMapping):
    """
    An LRUCache implementation backed by collections.OrderedDict
    """

    def __init__(self, max_size):
        self._cache = OrderedDict()
        self.max_size = max_size

    @property
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, n):
        for i in range(len(self._cache) - n):
            self._cache.popitem(False)
        self._max_size = n

    def __setitem__(self, key, value):
        if len(self._cache) >= self._max_size:
            self._cache.popitem(last=False)
        self._cache[key] = value

    if hasattr(OrderedDict, 'move_to_end'):
        def __getitem__(self, key):
            value = self._cache[key]
            self._cache.move_to_end(key)
            return value

    else:
        def __getitem__(self, key):
            value = self._cache[key] = self._cache.pop(key)
            return value

    def __delitem__(self, key):
        self._cache.__delitem__[key]

    def __iter__(self):
        return self._cache.__iter__()

    def __reversed__(self):
        return self._cache.__reversed__()

    def __len__(self):
        return self._cache.__len__()

    def __contains__(self, key):
        return self._cache.contains(key)

    def __getattr__(self, attr):
        return getattr(self._cache, attr)

    def update(self, other):
        MutableMapping.update(self, other)

    def copy(self):
        copy = self.__class__()
        copy._cache = self._cache.copy()
        return copy
