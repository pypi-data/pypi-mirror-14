"""
    Provide functions for accessing credential information from the config and keyring.
"""

import keyring

from .config import config


def get_credentials(uid):
    """
        Return the configured credentials for the virtual machine.

        :param str uid: name of the virtual machine

        :return: tuple of (username, password)
        :rtype: (str, str)
    """

    username = get_username(uid)
    password = get_password(username, uid)

    return username, password


def get_username(uid):
    """
        Return the username for the virtual machine.

        :param str uid: name of the virtual machine

        :return: username
        :rtype: str
    """

    if uid in config.machines and config.machines[uid].username:
        return config.machines[uid].username

    return config.credentials.username


def get_password(username, uid):
    """
        Return the password for the ``username`` and virtual machine.

        :param str username: username associated with the password
        :param str uid: name of the virtual machine

        :return: password
        :rtype: str
    """

    if uid in config.machines and config.machines[uid].password:
        return config.machines[uid].password
    elif _get_use_keyring(uid):
        password = _get_keyring_password(username, uid)

        if password:
            return password

    return config.credentials.password


def get_run_as_elevated(uid):
    """
        Return whether to run commands as an elevated user for virtual machine.

        :param str uid: name of the virtual machine

        :rtype: bool
    """

    if uid in config.machines and config.machines[uid].run_as_elevated is not None:
        return config.machines[uid].run_as_elevated

    return config.credentials.run_as_elevated


def _get_keyring_password(username, uid):
    """
        Return the password for the ``username`` and virtual machine from the keyring.

        :param str username: username associated with the password
        :param str uid: name of the virtual machine

        :return: password
        :rtype: str
    """

    if uid in config.machines:
        password = keyring.get_password(uid, username)

        if password:
            return password

    return keyring.get_password('vmupdate', username)


def _get_use_keyring(uid):
    """
        Return whether to use the keyring for virtual machine.

        :param str uid: name of the virtual machine

        :rtype: bool
    """

    if uid in config.machines and config.machines[uid].use_keyring is not None:
        return config.machines[uid].use_keyring

    return config.credentials.use_keyring
