import sys

from .posix import Posix


def get_shell(name, channel):
    shell_class = getattr(sys.modules[__name__], name)

    return shell_class(channel)
