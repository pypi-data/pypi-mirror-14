class ConfigSection(object):
    def __init__(self, data=None):
        self._data = data or {}

    def __getitem__(self, item):
        return self._data.get(item)

    def __contains__(self, item):
        return item in self._data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def items(self):
        return self._data.items()

    def iteritems(self):
        return self._data.iteritems()

    def iterkeys(self):
        return self._data.iterkeys()

    def itervalues(self):
        return self._data.itervalues()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()
