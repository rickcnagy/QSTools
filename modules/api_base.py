#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Base-level API interaction tools to be extended upon for different uses.
Generally, the intent is for extension towards the QS API, but this module
is designed to interaction with *any* REST API easier.
"""

import requests
import api_logging


class BaseRequest(object):
    """Generic base request for subclassing to handle any REST API.

    This class handles the actual process of making a request, allowing
    subclasses to only have to focus on making requests for the specific API
    that's being targetted.
    This class also handles logging, via api_logging, so subclasses should
    assume that all necessary data is being logged.
    Note that this class cannot be used by itself to make a request - it
    requires a subclass to set base_url.

    Static Attributes:
        Base attributes that will be included in all requests, and that should
        be overriden in subclasses and set per-request (if necessary) in
        prepare() or by overriding make_request():
            base_url
            base_params
            base_request_data
            base_headers

    Instance Attributes:
        uri: The URI string that the request is being made at. This will be
            appended to base_uri and so should be specific to the request.
            Generally, uri should begin with '/'.
        params: A dictionary of request-specific params to include.
        headers: A dictionary of request-specific headers to include.
        request_data: A dictionary of request-specific data to include.
        critical: A boolean indicating whether or not to exit if this request
            fails.
        silent: A boolean indicating whether or not this request should be
            logged or stay silent.
        verb: The HTTP verb to use, in all caps, such as: 'GET' or 'POST'
        base_uri:

        (filled after make_request())
        response: Raw, complete Request object. To check if the request has
            been made, check if response is not None.
        success: A boolean indicating whether the request was successful.
        data: The data cleaned from the request. This carries the actual body.
            of the data, and subclasses should ensure that if there's usable
            data in the response, self.data reflects this.
    """
    base_url = 'http://www.google.com'
    base_params = {}
    base_request_data = {}
    base_headers = {}

    def __init__(self, description, uri):
        self.description = description
        self.uri = uri

        self.params = {}
        self.request_data = {}
        self.headers = {}
        self.critical = False
        self.silent = False
        self.verb = 'GET'

        response = None
        text = None
        json = None
        data = None
        success = None
        status_code = None

    def make_request(self):
        """Make the request at the uri with specified data and params.

        If silent is False, then the data will be logged before and after the
        request with vital information. If critical is True, then if the
        request fails, sys.exit() will be called.

        Returns:
            The data received in the response. This reflects the actual body
            of the data, such as a list of students, not the success tag.
        """
        self.prepare()
        self._log_before()
        self.response = requests.request(
            self.verb,
            self._full_url(),
            params=self._full_params(),
            data=self._full_data(),
            headers=self._full_headers())
        self.process_response()
        self._log_after()
        return self.data

    def prepare(self):
        """Make any specific preparations to the request before making it.
        This should be overriden on a per-subclass basis to alter requests as
        necessary
        """
        pass

    def process_response(self):
        """Process the response after the fact and collect necessary info.
        This should be overridden to extract more info than success and data.
        """
        self.success = self.set_success()
        self.data = self.set_data()

    def set_data(self):
        """Set self.data based on the content of the response."""
        return self.response.json()

    def set_success(self):
        return self.response.status_code == 200

    def _log_before(self):
        if self.silent: return
        api_logging.info(self.description, self._log_dict(), is_request=True)

    def _log_after(self):
        if self.silent: return
        if self.success:
            api_logging.info(
                self.description,
                self._log_dict(),
                is_response=True)
        else:
            api_logging.error_or_critical(
                self.description,
                self._log_dict(),
                self.critical)

    def _log_dict(self):
        """The dict-based description of this request, mainly for logging"""
        desc = {
            'URI': self.uri,
            'full URI': self._full_uri(),
            'params': self._full_params(),
            'request data': self._full_data(),
            'headers': self._full_headers(),
            'verb': self.verb
        }
        if self.response:
            desc['response'] = self.response
            desc['HTTP status code'] = self.response.status_code
            desc['success'] = self.success
            desc['response data'] = self.data
        return desc

    def _full_url(self):
        return self.base_url + self.uri

    def _full_params(self):
        return self._merge_dicts([self.base_params, self.params])

    def _full_data(self):
        return self._merge_dicts([self.base_request_data, self.request_data])

    def _full_headers(self):
        return self._merge_dicts([self.base_headers, self.headers])

    def _merge_dicts(self, dicts):
        all_items = []
        for unmerged in dicts:
            for item in unmerged.items():
                all_items.append(item)
        return dict(all_items)
