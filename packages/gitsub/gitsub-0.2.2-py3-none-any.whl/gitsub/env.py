class Environment(object):
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def cleanup(self):
        self._cache.write()

    def __del__(self):
        try:
            self.cleanup()
        except Exception:
            pass
