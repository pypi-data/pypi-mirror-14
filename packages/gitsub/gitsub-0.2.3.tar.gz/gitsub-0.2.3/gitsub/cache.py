import os

class Cache(object):
    DEFAULT_CACHE_DIR = os.environ.get(
        "GITSUB_CACHE_DIR",
        os.path.expanduser("~/.cache/gitsub/")
    )

    def __init__(self, cache_name, directory=DEFAULT_CACHE_DIR): 
        super().__init__()
        self.cache_name = cache_name
        self.directory = directory
        self.content = ""

    def exists(self):
        return (self.dir_exists() and self.file_exists())

    def dir_exists(self):
        return os.path.exists(self.directory) and os.path.isdir(self.directory)

    def file_exists(self):
        file_path = os.path.join(self.directory, self.cache_name)
        return os.path.exists(file_path) and os.path.isfile(file_path)

    def save(self):
        """Write object dictionary to cache files in cache cache directory"""
        if not self.dir_exists():
            os.makedirs(self.directory, exist_ok=True)

        cache_file = os.path.join(
            self.directory,
            self.cache_name
        )

        with open(cache_file, "w") as f:
            if hasattr(self, "content"):
                print(self.content, end='', file=f)

    def load(self):
        """Fill object dictionary with cache files content in cache directory"""
        if not self.exists():
            self.save()

        cache_file = os.path.join(
            self.directory,
            self.cache_name
        )

        try:
            self.content = open(cache_file,"r").read()
        except IOError as ex:
            raise
