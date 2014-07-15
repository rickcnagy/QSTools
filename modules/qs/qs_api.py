#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
import re
from qs import QSRequest


class QSAPIWrapper(qs.APIWrapper):
    """An API Wrapper specific for the QuickSchools API.

    Attributes:
        live: Whether or not this is accessing the live QS server (or backup).
        schoolcode: The schoolcode that this wrapper is accessing.
        api_key: The API key being used for requests.

    Args:
        access_key: An API key or schoolcode to access the school by. If a
            schoolcode is supplied, its API key will be retrivied via
            qs.api_keys.
            If an API key is supplied, it will both be used here
            and then stored in the API key store for future use *if the request
            is successful*.
            The access_key defaults to `qstools` for convenience while testing,
            but since it's the first argument, `qs.API('someschool')` works to
            set a different school.
        live: Whether or not to use the live server.

    Note: in all instance methods, pass critical=True as a keyword argument to
    make any requests generated in that method critical, so that the script
    will exit (via logger.critical) if they fail.
    """

    def __init__(self, access_key='qstools', live=True):
        self._access_key = access_key
        self.live = live

        self.schoolcode = None
        self.api_key = None

        self._parse_access_key()

    # ============
    # = Students =
    # ============

    def get_students(self, desc='GET all students', **kwargs):
        """Get a list of all enrolled students from /students."""
        request = QSRequest(desc, '/students')
        return self.make_request(request, kwargs)

    def make_request(self, request, original_kwargs):
        """Process any QSRequest in this class and make it.

        Args:
            request: the prepared (but not yet made) QSRequest
            original_kwargs: the **kwargs passed to the function that
                instantiated this request, such as self.get_students().
        Returns:
            the data from the completed
        """
        request.set_api_key(self.api_key)
        if 'critical' in original_kwargs:
            request.critical = original_kwargs['critical']
        request.make_request()
        if request.successful:
            qs.api_keys.set(self._api_key_store_key_path(), self.api_key)
        return request

    def _parse_access_key(self):
        """Parses self._access key, which could be a schoolcode or API key, and
        set self.schoolcode and self.api_key.
        """
        # api keys are like schoolcode.blahblahblah
        match = re.match(r'(.+)\.', self._access_key)
        if match:
            self.schoolcode = match.groups()[0]
            self.api_key = self._access_key
        else:
            self.schoolcode = self._access_key
            self.api_key = qs.api_keys.get(self._api_key_store_key_path())

    def _api_key_store_key_path(self):
        live = 'live' if self.live else 'backup'
        return ['qs', live, self.schoolcode]
