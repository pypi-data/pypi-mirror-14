"""
######################
Space-Track API client
######################
"""

__author__ = 'Didier Alber'
__license__ = 'MIT'
__version__ = '0.1.1'


from .client import Client
from .exceptions import AuthenticationError, APIError


__all__ = [
    'Client',
    'AuthenticationError',
    'APIError'
]
