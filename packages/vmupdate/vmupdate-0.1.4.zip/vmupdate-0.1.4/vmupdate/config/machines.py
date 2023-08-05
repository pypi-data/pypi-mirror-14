from .configsection import ConfigSection


class Machines(ConfigSection):
    def __init__(self, data):
        self._data = {}

        if data:
            for name, machine_data in data.iteritems():
                self._data[name] = Machine(machine_data)


class Machine(ConfigSection):
    def __init__(self, data):
        super(Machine, self).__init__(data)

    @property
    def username(self):
        return self.get('Username')

    @property
    def password(self):
        return self.get('Password')

    @property
    def use_keyring(self):
        return self.get('Use Keyring')

    @property
    def run_as_elevated(self):
        return self.get('Run As Elevated')

    @property
    def shell(self):
        return self.get('Shell')
