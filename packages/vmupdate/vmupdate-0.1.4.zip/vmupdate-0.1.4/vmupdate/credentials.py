import keyring

from .config import config


def get_credentials(uid):
    username = get_username(uid)
    password = get_password(username, uid)

    return username, password


def get_username(uid):
    if uid in config.machines and config.machines[uid].username:
        return config.machines[uid].username

    return config.credentials.username


def get_password(username, uid):
    if uid in config.machines and config.machines[uid].password:
        return config.machines[uid].password
    elif get_use_keyring(uid):
        password = get_keyring_password(username, uid)

        if password:
            return password

    return config.credentials.password


def get_keyring_password(username, uid):
    if uid in config.machines:
        password = keyring.get_password(uid, username)

        if password:
            return password

    return keyring.get_password('vmupdate', username)


def get_use_keyring(uid):
    if uid in config.machines and config.machines[uid].use_keyring is not None:
        return config.machines[uid].use_keyring

    return config.credentials.use_keyring


def get_run_as_elevated(uid):
    if uid in config.machines and config.machines[uid].run_as_elevated is not None:
        return config.machines[uid].run_as_elevated

    return config.credentials.run_as_elevated
