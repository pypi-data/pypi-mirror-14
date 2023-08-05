from .configsection import ConfigSection


class PackageManagers(ConfigSection):
    def __init__(self, data):
        super(PackageManagers, self).__init__(data)
