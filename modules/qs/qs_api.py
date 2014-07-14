#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
import re


class QSAPIWrapper(qs.APIWrapper):
    """An API Wrapper specific for the QuickSchools API.

    Attributes:
        live: Whether or not this is accessing the live QS server (or backup).
        schoolcode: The schoolcode that this wrapper is accessing.
        api_key: The API key being used for requests.

    Args:
        access_key: An API key or schoolcode to access the school by. If a
            schoolcode is supplied, its API key will be retrivied via
            qs.api_keys. If an API key is supplied, it will both be used here
            and then stored in the API key store for future use.
        live: Whether or not to use the live server.
    """

    def __init__(self, access_key, live=True):
        self._access_key = access_key
        self.live = live

        self.schoolcode = None
        self.api_key = None

        self._parse_access_key()

    def _parse_access_key(self):
        """Parses self._access key, which could be a schoolcode or API key, and
        set self.schoolcode and self.api_key.
        """
        # api keys are like schoolcode.blahblahblah
        match = re.match(r'(.+)\.', self._access_key)
        if match:
            self.schoolcode = match.groups()[0]
            self.api_key = self._access_key
            qs.api_keys.set(self._api_key_store_key_path(), self._access_key)
        else:
            self.schoolcode = self._access_key
            self.api_key = qs.api_keys.get(self._api_key_store_key_path())

    def _api_key_store_key_path(self):
        live = 'live' if self.live else 'backup'
        return ['qs', live, self.schoolcode]
