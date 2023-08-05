"""
Throttler module tests
"""

import unittest
from time import time, sleep
from spacetrackapi.throttler import Throttler


class TestThrottler(unittest.TestCase):
    throttler_parameters = {
        'limit': 2,
        'time_interval': 2
    }
    """Default parameters for the throttler"""

    def test_blocking(self):
        """Tests the blocking version of the throttler"""

        t = Throttler(
            **self.throttler_parameters,
            blocking= True
        )

        start = time()
        t.allowed()
        t.allowed()
        t.allowed()
        self.assertGreaterEqual(
            time(),
            start + self.throttler_parameters['time_interval']
        )

    def test_nonblocking(self):
        """Tests the non-blocking version of the throttler"""

        t = Throttler(
            **self.throttler_parameters,
            blocking= False
        )

        self.assertTrue(t.allowed())
        self.assertTrue(t.allowed())
        self.assertFalse(t.allowed())


if __name__ == '__main__':
    unittest.main()
