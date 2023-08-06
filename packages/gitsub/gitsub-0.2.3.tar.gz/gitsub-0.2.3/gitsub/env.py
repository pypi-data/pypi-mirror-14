from gitsub.cache import Cache

class Environment(object):
    cache_dir = Cache.DEFAULT_CACHE_DIR
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def cleanup():
        pass

    def __del__(self):
        try:
            self.cleanup()
        except Exception:
            pass
