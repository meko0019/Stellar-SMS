class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class UserDoesNotExistError(Error):
    """Raised when the user in a query does not exist"""

    pass
