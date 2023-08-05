import os

class Cache(dict):
    DEFAULT_CACHE_DIR = os.environ.get(
        "GITSUB_CACHE_DIR",
        os.path.expanduser("~/.cache/gitsub/")
    )

    DEFAULT_CACHES = [ "repolist" ]

    def __init__(self, directory=DEFAULT_CACHE_DIR, caches=DEFAULT_CACHES):
        self.directory = directory
        self.caches = caches

    def exists(self):
        return (os.path.exists(self.directory) and
                all(os.path.exists(os.path.join(self.directory, cache))
                    for cache in self.caches)
                )

    def write(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)

        for cache in self.caches:
            cache_file = os.path.join(
                self.directory,
                cache
            )

            with open(cache_file, "w") as f:
                if cache in self:
                    print("\n".join(self[cache]), file=f)

    def read(self):
        if not os.path.exists(self.directory):
            raise IOError()

        for cache in self.caches:
            cache_file = os.path.join(
                self.directory,
                cache
            )

            try:
                self[cache] = open(cache_file,"r").read().splitlines()
            except IOError as ex:
                raise
