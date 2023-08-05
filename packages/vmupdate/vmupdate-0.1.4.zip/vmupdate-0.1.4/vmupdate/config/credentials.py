from .configsection import ConfigSection


class Credentials(ConfigSection):
    def __init__(self, data):
        super(Credentials, self).__init__(data)

    @property
    def username(self):
        return self.get('Username')

    @property
    def password(self):
        return self.get('Password')

    @property
    def use_keyring(self):
        return self.get('Use Keyring', False)

    @property
    def run_as_elevated(self):
        return self.get('Run As Elevated', False)
