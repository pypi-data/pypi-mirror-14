"""
********************
SpaceTrackAPI.client
********************

This module contains the client for the Space-Track API
"""

import re
import requests

from . import __version__
from . import urlbuilder
from .throttler import Throttler
from .exceptions import AuthenticationError, APIError


USER_AGENT = 'SpaceTrackAPI-Python-Client/' + __version__
"""str: User agent used for the client's requests"""


class Client(object):
    """Client for the Space-Track API

    Args:
        username (str): Username of the Space-Track account
        password (str): Password of the Space-Track account
    """


    def __init__(self, identity, password):
        # Login
        self._identity = identity

        # Password
        self._password = password

        # User agent
        self._user_agent = USER_AGENT

        # Session used for the API's calls
        self._requests = requests.Session()

        # Set the user agent
        self._requests.headers.update({
            'User-agent': self._user_agent
        })

        # throttler
        self._throttler = Throttler(
            limit= 19,
            time_interval= 60
        )

    @property
    def userAgent(self):
        """User agent used for the client's requests

        Args:
            str: New user agent

        Returns:
            str: User agent
        """

        return self._user_agent

    @userAgent.setter
    def userAgent(self, value):
        self._user_agent = value
        self._requests.headers.update({
            'User-agent': self.USER_AGENT
        })

    def blockingThrottle(self, blocking):
        """Set the blocking status of the requests

        Args:
            blocking (bool): True if the calls should be blocking.
                False if they should be non-blocking
        """

        self._throttler.blocking = blocking

    def authenticate(self):
        """Logs into the Space-Track API

        Raises:
            AuthenticationError: Failed authentication
        """

        if self._throttler.allowed():
            req = self._requests.post(urlbuilder.login(), {
                'identity': self._identity,
                'password': self._password
            })

            # Check if the authentication was successfull
            if req.status_code != 200:
                raise AuthenticationError(
                    'Authentication failed to the Space-Track API'
                )

    def logout(self):
        """Logs out of the Space-Track API"""

        if self._throttler.allowed():
            self._requests.get(urlbuilder.logout())

    def call(self, controller, action, request_class,
        predicates = {}, response_format = 'object', target_file = None, blocking = None):
        """Query the API

        Args:
            controller (str): Request controller
                'basicspacedata', 'expandedspacedata', 'fileshare'
            action (str): Request action
                'query', 'modeldef'
            request_class (str): Request class
            predicates (Optional[dict]): List of predicates
            response_format (Optional[string]): Response format,
                'json' (default), 'xml', 'html', 'csv', 'tle', '3le', 'kvn', 'dict'.
                'object' returns a python objet, as with json.load.
                By default : 'object'
            target_file (Optional[string]): If set to a file path,
                the response will be saved into this file
            blocking (Optional[bool]): Set the blocking status of this request

        Returns:
            Requests's response

        Raises:
            APIError: An error occurred during the call
        """

        # Format
        if response_format == 'object':
            request_format = 'json'
        else:
            request_format = response_format
        predicates.update({'format': request_format})

        # Building the request's url
        request_parameters = {
            'url': urlbuilder.build(
                controller,
                action,
                request_class,
                predicates
            ),
            'stream': bool(target_file)
        }

        if blocking != None:
            blocking_status = self._throttler.blocking
            self._throttler.blocking = bool(blocking)

        # If the call is non-blocking and the requests limit is attained, return None
        if not self._throttler.allowed():
            return None
        else:
            # Doing the request
            req = self._requests.get(**request_parameters)

            if blocking != None:
                self._throttler.blocking = blocking_status

            # Checking response
            if req.status_code == 401 and 'Unauthorized' not in req.text:
                # Not authenticated in the API
                # Authenticate then call the url again
                self.authenticate()
                req = self._requests.get(**request_parameters)

            if req.status_code >= 300:
                raise APIError(
                    # Remove HTML tags
                    re.sub('<.*?>', '', req.text).strip(),
                    req.status_code
                )

            if target_file:
                # Saving the response in a file
                with open(target_file, 'wb') as f:
                    for line in req.iter_content(1024):
                        f.write(line)

            elif response_format == 'object':
                # Returning a python object
                return req.json()
            else:
                # Returning the request's response
                return req.text

    def __enter__(self):
        """Authenticate in the API"""

        self.authenticate()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Log out of the API"""

        self.logout()
