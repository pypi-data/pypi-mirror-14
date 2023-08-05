"""
************************
SpaceTrackAPI.exceptions
************************

This module contains the exceptions of the Space-Track API
"""


class Error(Exception):
    """Base class for exceptions in the Space-Track API"""
    pass

class APIError(Error):
    """Raised when the API returns an error after a query"""
    def __init__(self, message, http_code, *args):
        self.message = message
        self.http_code = http_code
        super().__init__(message, http_code, *args)

class AuthenticationError(APIError):
    """Raised when the authentication to the Space-Track API fails"""

    def __init__(self, message, *args):
        super().__init__(message, 401, *args)
