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
    if uid in config.machines:
        if config.machines[uid].password:
            return config.machines[uid].password
        elif config.machines[uid].use_keyring == True:
            return keyring.get_password(uid, username)
        elif config.machines[uid].use_keyring == False:
            return config.credentials.password

    if config.credentials.use_keyring:
        return keyring.get_password('vmupdate', username)

    return config.credentials.password

def get_run_as_elevated(uid):
    if uid in config.machines and config.machines[uid].run_as_elevated is not None:
        return config.machines[uid].run_as_elevated

    return config.credentials.run_as_elevated
