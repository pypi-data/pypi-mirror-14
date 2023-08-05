from .configsection import ConfigSection


class General(ConfigSection):
    def __init__(self, data):
        super(General, self).__init__(data)

    @property
    def wait_after_start(self):
        return self['Wait After Start']
