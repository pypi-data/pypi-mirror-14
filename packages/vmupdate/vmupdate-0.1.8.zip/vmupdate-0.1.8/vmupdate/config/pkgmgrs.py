"""
    Provide a wrapper around the package managers configuration section.
"""

from .configsection import ConfigSection


class PackageManagers(ConfigSection):
    def __init__(self, data):
        super(PackageManagers, self).__init__(data)
