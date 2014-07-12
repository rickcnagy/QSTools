#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
import re


class API(object):
    """The class for interacting with the QS REST API.
    One API object should be created per server/subdomain - i.e. one object for
    school A on the live server, another for school B on the live server, and a
    third for school A on the backup server.

    Attributes:
        schoolcode: the schoolcode being accessed
        api_key: the API key used for access
        live: whether or not to use the live server
    """

    def __init__(self, access_key, live=True):
        """access_key can either be a schoolcode or API key"""
        self._access_key = access_key

    def get_students(self):
        pass

    def _process_access_key(self, access_key):
        """Processes an access key, which could be a schoolcode or API key
        Note that API keys are like schoolcode.blahblahblah

        Returns:
            A tuple, with the schoolcode followed by the API key
        """
        # api keys are like schoolcode.blahblahblah
        match = re.match(r'(.+)\.', access_key)
        if match:
            return re.groups()[0], access_key
        else:
            return access_key, self._get_api_key(access_key)

    def _get_api_key(self, schoolcode):
        """Get the API key on file for that schoolcode"""
        #TODO: implement

