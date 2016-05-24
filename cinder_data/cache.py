class Cache(object):

    def get_record(self, name, record_id):
        raise NotImplementedError()

    def set_record(self, name, record_id, record):
        raise NotImplementedError()


class MemoryCache(Cache):
    """docstring for MemoryCache"""
    def __init__(self):
        super(MemoryCache, self).__init__()
        self._cache = {}

    def get_record(self, name, record_id):
        if name in self._cache:
            if record_id in self._cache[name]:
                return self._cache[name][record_id]

    def set_record(self, name, record_id, record):
        if name not in self._cache:
            self._cache[name] = {}
        self._cache[name][record_id] = record
