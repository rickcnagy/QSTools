#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

from qs import *


class API(object):
    """The class for interacting with the QS REST API.
    One API object should be created per server/subdomain - i.e. one object for
    school A on the live server, another for school B on the live server, and a
    third for school A on the backup server.
    """

    def __init__(self, schoolcode, live=True):
        pass

    def get_students(self):
        pass
