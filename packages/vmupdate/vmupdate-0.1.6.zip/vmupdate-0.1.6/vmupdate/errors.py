class AppError(Exception):
    pass


class SshError(AppError):
    pass


class UpdateError(AppError):
    pass
