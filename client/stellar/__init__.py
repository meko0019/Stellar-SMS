class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class UnknownIssuerError(Error):
    """Raised when the issuer can't be verified"""

    pass
