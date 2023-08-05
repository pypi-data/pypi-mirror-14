from .configsection import ConfigSection


class Network(ConfigSection):
    def __init__(self, data):
        super(Network, self).__init__(data)

        self._ssh = Ssh(self._data['SSH'])

    @property
    def ssh(self):
        return self._ssh


class Ssh(ConfigSection):
    def __init__(self, data):
        super(Ssh, self).__init__(data)

    @property
    def guest_port(self):
        return self['Guest']['Port']

    @property
    def host_min_port(self):
        return self['Host']['Ports']['Min']

    @property
    def host_max_port(self):
        return self['Host']['Ports'].get('Max', 65535)
