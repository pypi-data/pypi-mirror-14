"""
    Provide a wrapper around the virtualizers configuration section.
"""

from .configsection import ConfigSection


class Virtualizers(ConfigSection):
    def __init__(self, data):
        super(Virtualizers, self).__init__(data)
