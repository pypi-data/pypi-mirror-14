"""
    Provide a wrapper around configuration.
"""

import logging.config
import os
import pkgutil

import yaml

from vmupdate import BASE_DIR


class ConfigSection(object):
    """
        Provide a base class for configuration sections.

        This class wraps a :class:`dict`.
    """

    def __init__(self, data=None):
        """
            Return an instance of :class:`ConfigSection`.

            :param dict data: the data for the config section

            :rtype:`ConfigSection`
        """

        self._data = data or {}

    def __getitem__(self, key):
        """Return the value for ``key``, else ``None``."""

        return self._data.get(key)

    def __contains__(self, key):
        """Return ``True`` if the config section contains ``key``, else ``False``."""

        return key in self._data

    def __iter__(self):
        """Return an iterator over the keys of the config section."""

        return iter(self._data)

    def __len__(self):
        """Return the number of items in the config section."""

        return len(self._data)

    def get(self, key, default=None):
        """Return the value for ``key``, else ``default``."""

        return self._data.get(key, default)

    def items(self):
        """Return a copy of the config section's list of (key, value) pairs."""

        return self._data.items()

    def iteritems(self):
        """Return an iterator over the config section's (key, value) pairs."""

        return self._data.iteritems()

    def iterkeys(self):
        """Return an iterator over the config section's keys."""

        return self._data.iterkeys()

    def itervalues(self):
        """Return an iterator over the config section's values."""

        return self._data.itervalues()

    def keys(self):
        """Return a copy of the config section's list of keys."""

        return self._data.keys()

    def values(self):
        """Return a copy of the config section's list of values."""

        return self._data.values()


class Credentials(ConfigSection):
    """Provide a wrapper around the credentials configuration section."""

    def __init__(self, data):
        """
            Return an instance of :class:`Credentials`.

            This method extends :meth:`ConfigSection.__init__`.

            :param dict data: the data for the config section

            :rtype:`Credentials`
        """

        super(Credentials, self).__init__(data)

    @property
    def username(self):
        """
            Return the *Username* configuration.

            :rtype: str
        """

        return self.get('Username')

    @property
    def password(self):
        """
            Return the *Password* configuration.

            :rtype: str
        """

        return self.get('Password')

    @property
    def use_keyring(self):
        """
            Return the *Use Keyring* configuration.

            :rtype: bool
        """

        return self.get('Use Keyring', False)

    @property
    def run_as_elevated(self):
        """
            Return the *Run As Elevated* configuration.

            :rtype: bool
        """

        return self.get('Run As Elevated', False)


class General(ConfigSection):
    """Provide a wrapper around the general configuration section."""

    def __init__(self, data):
        """
            Return an instance of :class:`General`.

            This method extends :meth:`ConfigSection.__init__`.

            :param dict data: the data for the config section

            :rtype:`General`
        """

        super(General, self).__init__(data)

    @property
    def wait_after_start(self):
        """
            Return the *Wait After Start* configuration.

            :rtype: int
        """

        return self['Wait After Start']

    @property
    def wait_before_stop(self):
        """
            Return the *Wait Before Stop* configuration.

            :rtype: int
        """

        return self['Wait Before Stop']


class Machines(ConfigSection):
    """
        Provide a wrapper around the machines configuration section.

        This class wraps a dict of :class:`Machine`.
    """

    def __init__(self, data):
        """
            Return an instance of :class:`Machines`.

            This method extends :meth:`ConfigSection.__init__`.

            :param dict data: the data for the config section

            :rtype:`Machines`
        """

        super(Machines, self).__init__(data)

        if data:
            for name, machine_data in data.iteritems():
                self._data[name] = Machine(machine_data)


class Machine(ConfigSection):
    """Provide a wrapper around the machine configuration section."""

    def __init__(self, data):
        """
            Return an instance of :class:`Machine`.

            This method extends :meth:`ConfigSection.__init__`.

            :param dict data: the data for the config section

            :rtype:`Machine`
        """

        super(Machine, self).__init__(data)

    @property
    def username(self):
        """
            Return the *Username* configuration.

            :rtype: str
        """

        return self.get('Username')

    @property
    def password(self):
        """
            Return the *Password* configuration.

            :rtype: str
        """

        return self.get('Password')

    @property
    def use_keyring(self):
        """
            Return the *Use Keyring* configuration.

            :rtype: bool
        """

        return self.get('Use Keyring')

    @property
    def run_as_elevated(self):
        """
            Return the *Run As Elevated* configuration.

            :rtype: bool
        """

        return self.get('Run As Elevated')

    @property
    def shell(self):
        """
            Return the *Shell* configuration.

            :rtype: str
        """

        return self.get('Shell')


class Network(ConfigSection):
    """Provide a wrapper around the network configuration section."""

    def __init__(self, data):
        """
            Return an instance of :class:`Network`.

            This method extends :meth:`ConfigSection.__init__`.

            :param dict data: the data for the config section

            :rtype:`Network`
        """

        super(Network, self).__init__(data)

        self._ssh = Ssh(self._data['SSH'])

    @property
    def ssh(self):
        """
            Return the *SSH* configuration section.

            :rtype: :class:`Ssh`
        """

        return self._ssh


class Ssh(ConfigSection):
    """Provide a wrapper around the SSH configuration section."""

    def __init__(self, data):
        """
            Return an instance of :class:`Ssh`.

            This method extends :meth:`ConfigSection.__init__`.

            :param dict data: the data for the config section

            :rtype:`Ssh`
        """

        super(Ssh, self).__init__(data)

    @property
    def guest_port(self):
        """
            Return the guest port configuration.

            :rtype: int
        """

        return self['Guest']['Port']

    @property
    def host_min_port(self):
        """
            Return the host port minimum configuration.

            :rtype: int
        """

        return self['Host']['Ports']['Min']

    @property
    def host_max_port(self):
        """
            Return the host port maximum configuration, else 65,535.

            :rtype: int
        """

        return self['Host']['Ports'].get('Max', 65535)


class PackageManagers(ConfigSection):
    """Provide a wrapper around the package managers configuration section."""

    def __init__(self, data):
        """
            Return an instance of :class:`PackageManagers`.

            This method extends :meth:`ConfigSection.__init__`.

            :param dict data: the data for the config section

            :rtype:`PackageManagers`
        """

        super(PackageManagers, self).__init__(data)


class Shells(ConfigSection):
    """Provide a wrapper around the shells configuration section."""

    def __init__(self, data):
        """
            Return an instance of :class:`Shells`.

            This method extends :meth:`ConfigSection.__init__`.

            :param dict data: the data for the config section

            :rtype:`Shells`
        """

        super(Shells, self).__init__(data)


class Virtualizers(ConfigSection):
    """Provide a wrapper around the virtualizers configuration section."""

    def __init__(self, data):
        """
            Return an instance of :class:`Virtualizers`.

            This method extends :meth:`ConfigSection.__init__`.

            :param dict data: the data for the config section

            :rtype:`Virtualizers`
        """

        super(Virtualizers, self).__init__(data)


class Config(ConfigSection):
    """Provide a wrapper for the merged configuration files."""

    def __init__(self):
        super(Config, self).__init__()

        self._general = None
        self._credentials = None
        self._network = None
        self._virtualizers = None
        self._pkgmgrs = None
        self._shells = None
        self._machines = None

        self._logging = None

    @property
    def general(self):
        """
            Return the *General* configuration section.

            :rtype: :class:`General`
        """

        return self._general

    @property
    def credentials(self):
        """
            Return the *Credentials* configuration section.

            :rtype: :class:`Credentials`
        """

        return self._credentials

    @property
    def network(self):
        """
            Return the *Network* configuration section.

            :rtype: :class:`Network`
        """

        return self._network

    @property
    def virtualizers(self):
        """
            Return the *Virtualizers* configuration section.

            :rtype: :class:`Virtualizers`
        """

        return self._virtualizers

    @property
    def pkgmgrs(self):
        """
            Return the *Package Managers* configuration section.

            :rtype: :class:`PackageManagers`
        """

        return self._pkgmgrs

    @property
    def shells(self):
        """
            Return the *Shells* configuration section.

            :rtype: :class:`Shells`
        """

        return self._shells

    @property
    def machines(self):
        """
            Return the *Machines* configuration section.

            :rtype: :class:`Machines`
        """

        return self._machines

    def load(self, config_path=None, log_dir=None):
        """
            Load the configuration files and configure logging.

            :param str config_path: path to a user defined configuration file
            :param str log_dir: path to the directory where log files are to be stored
        """

        default_config = yaml.load(pkgutil.get_data('vmupdate', 'data/vmupdate.yaml'))

        if config_path:
            with open(config_path, 'r') as config_file:
                user_config = yaml.load(config_file)

            self._data = _merge(default_config, user_config)
        else:
            self._data = default_config

        self._general = General(self._data['General'])
        self._credentials = Credentials(self._data['Credentials'])
        self._network = Network(self._data['Network'])
        self._virtualizers = Virtualizers(self._data['Virtualizers'])
        self._pkgmgrs = PackageManagers(self._data['Package Managers'])
        self._shells = Shells(self._data['Shells'])
        self._machines = Machines(self._data['Machines'])

        self._logging = yaml.load(pkgutil.get_data('vmupdate', 'data/logging.yaml'))

        if not log_dir:
            log_dir = BASE_DIR

        self._set_log_filename(log_dir, 'info_file')
        self._set_log_filename(log_dir, 'error_file')

        logging.config.dictConfig(self._logging)

    def _set_log_filename(self, log_dir, handler_name):
        """
            Update the log handler to write to the specified directory.

            :param str log_dir: path to the directory where log files are to be stored
            :param str handler_name: name of the log handler to update
        """

        if handler_name in self._logging['handlers']:
            self._logging['handlers'][handler_name]['filename'] =\
                os.path.join(log_dir, self._logging['handlers'][handler_name]['filename'])


def _merge(a, b):
    """
        Return the merge of two dictionaries.

        :param dict a: dictionary to merge into
        :param dict b: dictionary to merge

        :rtype: dict
    """

    if b is None:
        return a

    if isinstance(a, dict):
        for key in b:
            if key in a:
                a[key] = _merge(a[key], b[key])
            else:
                a[key] = b[key]
    else:
        a = b

    return a


config = Config()
