"""
    Provide application-specific error classes.
"""


class AppError(Exception):
    """Provide base class for application-specific errors."""
    pass


class SshError(AppError):
    """Provide class for SSH errors."""
    pass


class UpdateError(AppError):
    """Provide class for update errors."""
    pass
