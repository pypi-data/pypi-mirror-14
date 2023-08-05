"""
***********************
SpaceTrackAPI.throttler
***********************

This module contains the throttler limiting requests to the Space-Track API

If the limit is attained, the throttler sleeps until enough time
has passed that a new request can be done

See the Space-Track documentation for the complete limits :
https://www.space-track.org/documentation
"""


from time import time, sleep
from collections import deque


class Throttler(object):
    """Throttler for the Space-Track API

    Args:
        limit (int): Maximum number of requests
        time_interval (int): Time interval of the limit, in seconds
        blocking (Optional[bool]): If False,
            when the limit is reached the throttler will not sleep.
            The allowed() function will return True if a request can be made, False if not
    """

    blocking = True
    """bool: Blocking status of the throttler"""

    def __init__(self, limit, time_interval, blocking = True):
        # limit
        self._limit = int(limit)
        if self._limit <= 0:
            raise ValueError('Incorrect parameter "limit" : ' + limit)

        # time_interval
        self._time_interval = int(time_interval)
        if self._time_interval <= 0:
            raise ValueError(
                'Incorrect parameter "time_interval" : ' + time_interval
            )

        # blocking
        self.blocking = bool(blocking)

        # Logging queue
        self._log = deque()

    def allowed(self):
        """Check if a new request can be done

        If blocking, the throttler will sleep until a new request ca be done.
        If non blocking, this function will return
        True if a request can be done,
        False if the limit is attained.

        Returns:
            bool: True if a request can be done, False otherwise
        """

        if self.blocking:
            self._wait()
            do_request = True
        else:
            self._cleanLog()
            do_request = len(self._log) < self._limit

        if do_request:
            self._log.append(time())

        return do_request

    def _cleanLog(self):
        """Cleans the requests log

        Remove the requests older than self._time_interval seconds from the log
        """

        while len(self._log) > 0 and self._log[0] < time() - self._time_interval:
            self._log.popleft()

    def _wait(self):
        """Wait until a new request can be done"""

        self._cleanLog()

        while len(self._log) >= self._limit:
            waiting_time = time() - self._log[0] + self._time_interval
            if waiting_time > 0:
                sleep(waiting_time)

            self._cleanLog()
