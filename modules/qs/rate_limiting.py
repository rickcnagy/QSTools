#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Limit request rates on REST servers by request base URL."""

import time
import requests
from qs import logger

_QS_LIVE_LIMIT = 5
_QS_LIVE_WAIT_TIME = 1
_QS_BACKUP_LIMIT = 100
_QS_BACKUP_WAIT_TIME = 0
_GITHUB_LIMIT_HEADER = 'X-RateLimit-Remaining'


# {server_id: _ServerWithKnownLimit}
_servers = {}


def process_request(request_url):
    """Process a request that's about to me made, which will automatically
    trigger a wait (or whatever else for that server) when appropriate
    """
    server = _lookup_server(request_url)
    if not server:
        logger.warning('Tried to make a request at an unrecognized URL', url)
    else:
        server.register_request(request_url)


def process_response(response):
    """Process a response that was received by the server. Any appriate action
    will be taken based on the response itself.

    Args:
        response: a completed response object
    """
    url = response.url()
    server = _lookup_server(url)
    if not server:
        logger.warning('Received a response at an unrecognized URL', url)
    else:
        server.register_response(response)


def get_server(request_url):
    _init_servers()
    if 'quickschools.com' in request_url:
        return _servers['qs_live']
    elif 'smartschoolcentral.com' in request_url:
        return _servers['qs_backup']
    elif 'github.com' in request_url:
        return _servers['github']

# =============
# = Protected =
# =============


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
        'github': _HeaderBasedServer(_GITHUB_LIMIT_HEADER)
    }
    return _servers


class _ServerWithLimit(object):
    """A class to keep track of rate limits on a server.

    register_request should be called right before every call to the server,
    and it will automatically trigger _limit_reached automatically.

    This should be subclassed (in this file) to change behavior for different
    servers/behaviors.
    """

    def __init__(self, identitifer):
        self._identifier = identifier
        self._request_count = 0
        self._response_count = 0
        self._limit_has_been_reached = False

    def register_request(self, request):
        self._request_count += 1

    def register_response(self, response):
        self._response_count += 1

    def _limit_reached(self):
        self._limit_has_been_reached = True
        logger.critical(
            'Tried to make request, but limit reached for server',
            self._identifier)


class _ServerWithKnownLimit(object):
    """A server with a known limit ahead of time

    e.g. 5 requests then 1 wait
    """

    def __init__(self, identifier, limit):
        self._limit = limit
        super(_ServerWithKnownLimit, self).__init__(identifier)

    def register_request(self, request):
        super(_ServerWithKnownLimit, self).register_request(request)
        if self._request_count >= self._limit:
            self._request_count = 0
            self._limit_reached()


class _ServerWithWait(_ServerWithKnownLimit):
    """A server that requires waits between calls, such as QS."""

    def __init__(self, identifier, limit, wait_time):
        """Wait time is in seconds"""
        self._wait_time = wait_time
        super(_ServerWithWait, self).__init__(identifier, limit)

    def _limit_reached(self):
        time.sleep(self._wait_time)


class _HeaderBasedServer(_ServerWithLimit):
    """A server where action is taken based on the headers of responses"""

    def __init__(self, identifier, remaining_header_field):
        """remaining_header_field is the header field that indicates the number
        of responses left.
        """
        self._remaining_header_field = remaining_header_field
        self._should_terminate = False
        self.remaining = None
        super(_HeaderBasedServer, self).__init__(identifier, 0)

    def register_request(self, request):
        super(_HeaderBasedServer, self).register_response(response)
        if self._should_terminate:
            self._limit_reached()

    def register_response(self, response):
        super(_HeaderBasedServer, self).register_response(response)
        self.remaining = response.headers[self._remaining_header_field]
        import pudb; pudb.set_trace()
        # TODO: figure out if int or str and set _should_terminate
