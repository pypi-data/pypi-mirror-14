import os
from gitsub.cache import Cache

class Environment(object):
    cache_dir = Cache.DEFAULT_CACHE_DIR

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    @property
    def cache(self):
        if not hasattr(self, "_cache"):
            self._cache = Cache(directory=self.cache_dir)
            if not self._cache.exists():
                self._cache.write()
            self._cache.read()
        return self._cache

    def cleanup(self):
        self._cache.write()

    def __del__(self):
        try:
            self.cleanup()
        except Exception:
            pass
