#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
import re


class API(object):
    """The class for interacting with the QS REST API.
    One API object should be created per server/subdomain - i.e. one object for
    school A on the live server, another for school B on the live server, and
    third for school A on the backup server.

    (Public) Attributes:
        schoolcode: the schoolcode being accessed
        api_key: the API key used for access
        live: whether or not to use the live server
    """

    def __init__(self, access_key, live=True):
        """Args:
                access_key: the schoolcode or API key to access the QS API. If
                    it's a schoolcode, api_key_store.py will try to lookup the
        """
        self._access_key = access_key
        self.live = live

        self.schoolcode = None
        self.api_key = None

        self._process_access_key()

    def get_students(self):
        """"""




    # =============
    # = Protected =
    # =============

    def _process_access_key(self):
        """Processes the access key, which could be a schoolcode or API key
        Note that API keys are like schoolcode.blahblahblah

        Sets self.schoolcode and self.api_key
        """
        # api keys are like schoolcode.blahblahblah
        match = re.match(r'(.+)\.', self._access_key)
        if match:
            self.schoolcode = match.groups()[0]
            self.api_key = self._access_key
        else:
            self.schoolcode = self._access_key
            self.api_key = self._get_api_key(self._access_key)

    def _get_api_key(self, schoolcode):
        """Get the API key on file for that schoolcode"""
        #TODO: implement, as follows:
        """setup.py should add a file: ~/QuickSchools API Keys.json which is
        formatted like:
        {schoolcode: api_key, schoolcode-bak: api_key, pld: api_key, github: api_key}
        and created (with dummy data only) during setup.py

        then, a module called api_key_access.py accesses that file (or remakes
        it) and tries to lookup the schoolcode with matching live value. If it
        is found, it's returned here, but if isn't, api_key_store.py gracefully
        exits the script with a correct error, and writes to the log.

        api_key_store can access both QS and non qs api keys - it's just a key
        value store.
        """
        raise NotImplementedError('Need to supply an API Key to qs.API()')
