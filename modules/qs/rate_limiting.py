#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Limit request rates on REST servers by request base URL."""

import time
import requests
import qs

_QS_LIVE_LIMIT = 5
_QS_LIVE_WAIT_TIME = 1
_QS_BACKUP_LIMIT = 100
_QS_BACKUP_WAIT_TIME = 0
_GITHUB_LIMIT_HEADER = 'X-RateLimit-Remaining'


# {server_id: _ServerWithKnownLimit}
_servers = {}


def register_request(request_url):
    """Process a request that's about to me made, which will automatically
    trigger a wait (or whatever else for that server) when appropriate
    """
    server = get_server(request_url)
    if server:
        server.register_request(request_url)


def register_response(response):
    """Process a response that was received by the server. Any appriate action
    will be taken based on the response itself.

    Args:
        response: a completed response object
    """
    url = response.url
    server = get_server(url)
    if server:
        server.register_response(response)


def get_server(url):
    _init_servers()
    if 'quickschools' in url:
        return _servers['qs_live']
    elif 'smartschoolcentral' in url:
        return _servers['qs_backup']
    elif 'github' in url:
        return _servers['github']
    elif 'httpbin' in url:
        return _servers['httpbin']
    elif 'localhost' in url:
        return _servers['localhost']
    qs.logger.warning(
        'Making request/response at unrecognized URL, so no '
        'rate limiting or request tracking is in place for', url)

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
        'github': _HeaderBasedServer(
            'github',
            _GITHUB_LIMIT_HEADER),
        'httpbin': _Server('httpbin'),
        'localhost': _Server('localhost'),
    }
    return _servers


class _Server(object):
    """A server to make requests at. Rate limiting may not be necessary."""

    def __init__(self, identifier):
        self.identifier = identifier
        self.request_count = 0
        self.response_count = 0

    def register_request(self, request_url):
        self.request_count += 1

    def register_response(self, response):
        self.response_count += 1


class _ServerWithLimit(_Server):
    """A server with a rate limit.g

    register_request should be called right before every call to the server,
    and it will automatically trigger _limit_reached automatically.

    This should be subclassed (in this file) to change behavior for different
    servers/behaviors.
    """

    def __init__(self, identifier):
        self._limit_has_been_reached = False
        super(_ServerWithLimit, self).__init__(identifier)

    def _limit_reached(self):
        self._limit_has_been_reached = True
        qs.logger.critical(
            'Tried to make request, but limit reached for server',
            self.identifier)


class _ServerWithKnownLimit(_ServerWithLimit):
    """A server with a known limit ahead of time

    e.g. 5 requests then 1 wait
    """

    def __init__(self, identifier, limit):
        self._limit = limit
        super(_ServerWithKnownLimit, self).__init__(identifier)

    def register_request(self, request_url):
        super(_ServerWithKnownLimit, self).register_request(request_url)
        if self.request_count >= self._limit:
            self.request_count = 0
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
        super(_HeaderBasedServer, self).__init__(identifier)

    def register_request(self, request_url):
        super(_HeaderBasedServer, self).register_request(request_url)
        if self._should_terminate:
            self._limit_reached()

    def register_response(self, response):
        super(_HeaderBasedServer, self).register_response(response)
        self.remaining = response.headers[self._remaining_header_field]
        self._should_terminate = self.remaining != '0'
