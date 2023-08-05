import pkg_resources
from . import __version__

def get_version():
    return __version__

def sub_output(completed):
    return completed.stdout.rstrip('\n')
