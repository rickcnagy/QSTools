#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Limit request rates on REST servers by request base URL."""

import time

_QS_LIVE_LIMIT = 5
_QS_LIVE_WAIT_TIME = 1
_QS_BACKUP_LIMIT = 100
_QS_BACKUP_WAIT_TIME = 0


# {server_id: _ServerWithLimit}
_servers = {}


def process_request(base_url):
    """Process a request that's been made at base_url, which will automatically
    trigger a wait (or whatever else for that server) when appropriate
    """
    _init_servers()
    if 'quickschools.com' in base_url:
        _servers['qs_live'].register_request()
    elif 'smartschoolcentral.com' in base_url:
        _servers['qs_backup'].register_request()
    else:
        raise KeyError('{} is not a valid server URL'.format(base_url))


def _init_servers():
    global _servers
    _servers = _servers or {
        'qs_live': _ServerWithWait(
            'qs_live',
            _QS_LIVE_LIMIT,
            _QS_LIVE_WAIT_TIME),
        'qs_backup': _ServerWithWait(
            'qs_backup',
            _QS_BACKUP_LIMIT,
            _QS_BACKUP_WAIT_TIME),
    }
    return _servers


class _ServerWithLimit(object):
    """A class to keep track of rate limits on a server.

    register_request should be called right before every call to the server,
    and it will automatically trigger _limit_reached after the request limit
    is reached.

    This should be subclassed (in this file) to change behavior for different
    servers/behaviors.
    """

    def __init__(self, identifier, limit):
        self._identifier = identifier
        self._limit = limit

        self._request_count = 0

    def register_request(self):
        self._request_count += 1
        if self._request_count >= self._limit:
            self._request_count = 0
            self._limit_reached()

    def _limit_reached(self):
        sys.exit('Limit reached for server {}'.format(self._identifier))


class _ServerWithWait(_ServerWithLimit):
    """A server that requires waits between calls, such as QS."""

    def __init__(self, identifier, limit, wait_time):
        """Wait time is in seconds"""
        self._wait_time = wait_time
        super(_ServerWithWait, self).__init__(identifier, limit)

    def _limit_reached(self):
        time.sleep(self._wait_time)
