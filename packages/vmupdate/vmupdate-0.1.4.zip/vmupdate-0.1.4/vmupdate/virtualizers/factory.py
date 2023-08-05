import sys

from .virtualbox import VirtualBox


def get_virtualizer(name, path):
    virtualizer_class = getattr(sys.modules[__name__], name)

    return virtualizer_class(path)
