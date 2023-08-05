"""
UrlBuilder module tests
"""

import json
import unittest
from unittest.mock import patch, Mock, create_autospec

import requests

from spacetrackapi import Client, AuthenticationError, APIError
from spacetrackapi.throttler import Throttler


class TestClient(unittest.TestCase):
    build_parameters = {
        'controller': 'basicspacedata',
        'action': 'query',
        'request_class': 'satcat',
        'predicates': {
            'LAUNCH': '>now-7',
            'CURRENT': 'Y',
            'orderby': 'LAUNCH DESC'
        },
        'response_format': 'json'
    }
    """Default parameters for Client.call()"""


    def setSessionResponse(self, status_code=200, content=''):
        """Define the Session's object response

        Args:
            status_code (int): Status code of the response
            content (str): Content of the response
        """

        instance = self._mock_session.return_value

        instance.post.return_value.status_code = status_code
        instance.post.return_value.text = content

        instance.get.return_value.status_code = status_code
        instance.get.return_value.text = content

    def setUp(self):
        """Set up the mock Session instance"""

        self._patcher = patch('requests.Session', autospec=True)
        self._mock_session = self._patcher.start()
        instance = self._mock_session.return_value
        # Add "headers" attribute
        instance.headers = {}
        # By default, return a successfull response
        self.setSessionResponse(200)

    def tearDown(self):
        """Stop the mock Session instance"""

        self._patcher.stop()

    def test_login(self):
        """Tests a successfull login"""

        client = Client('username', 'password')
        self.setSessionResponse(200)
        try:
            client.authenticate()
        except Exception as e:
            self.fail("Exception raised : " + str(e))

    def test_login_fail(self):
        """Tests an incorrect login"""

        client = Client('username', 'password')
        self.setSessionResponse(401)
        with self.assertRaises(AuthenticationError):
            client.authenticate()

    def test_call_unauthenticated(self):
        """Tests an unauthenticated API call"""

        with Client('username', 'password') as client:
            self.setSessionResponse(401)
            with self.assertRaises(APIError):
                data = client.call(**self.build_parameters)

    def test_call_httperror(self):
        """Tests an API error"""

        with Client('username', 'password') as client:
            self.setSessionResponse(500)
            with self.assertRaises(APIError):
                data = client.call(**self.build_parameters)

    def test_call(self):
        """Tests a correct call"""

        with Client('username', 'password') as client:
            self.setSessionResponse(content='{"ok": true}')
            data = client.call(**self.build_parameters)
            self.assertEqual(data, '{"ok": true}')

    def test_throttling(self):
        """Test the throttling"""

        client = Client('username', 'password')
        # Define a non-blocking throttler
        # with a limit of 3 requests within 2 seconds
        client._throttler = Throttler(3, 2, False)

        client.authenticate()
        self.assertNotEqual(
            client.call(**self.build_parameters),
            None
        )
        self.assertNotEqual(
            client.call(**self.build_parameters),
            None
        )
        self.assertEqual(
            client.call(**self.build_parameters),
            None
        )



if __name__ == '__main__':
    unittest.main()
