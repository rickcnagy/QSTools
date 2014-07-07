#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Base-level API interaction tools to be extended upon for different uses.
Generally, the intent is for extension towards the QS API, but this module
is designed to interaction with *any* REST API easier.
"""

import requests
import api_logging

# abstractions from requests to prevent importing of requests module
get = requests.get
post = requests.post
put = requests.put
delete = requests.delete

class BaseRequest(object):
    """Generic base request for subclassing to handle any REST API.

    This class handles the actual process of making a request, allowing
    subclasses to only have to focus on making requests for the specific API
    that's being targetted.
    This class also handles logging, via api_logging, so subclasses should
    assume that all necessary data is being logged.

    Attributes:
        uri: The URI string that the request is being made at
        params: A dictionary of params to include in the request
        request_data: A dictionary of data to include in the body
        critical: A boolean indicating whether or not to exit if this request
            fails.
        silent: A boolean indicating whether or not this request should be
            logged or stay silent.
        request_func: The function used to make the request.

        (available after make_request())
        response: Raw, complete Request object.
        text: The ra textual representation of the response's full body.
        json: The raw dictionary representation of the response's full body.
        data: The data cleaned from the request. This carries the actual body.
            of the data, and subclasses should ensure that if there's usable
            data in the response, self.data reflects this.
        success: A boolean indicating whether the request was successful.
        status_code: An integer representation of the response's status code.
    """

    def __init__(self, description, uri):
        self.description = description
        self.uri = uri

        self.params = {}
        self.request_data = {}
        self.critical = False
        self.silent = False
        self.request_func = get
