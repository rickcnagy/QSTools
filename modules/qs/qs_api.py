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

    Methods that involve an API call have a set of kwargs that can be applied:
        critical: If True, then logger.critical will be called upon failure.
        fields: A list or string of fields to add to the 'fields' param.
        no_cache: (request-specific) If True, the cache will be ignored and
            reset for that resource.
        by_id: (request with list result specific) If True, return the data in
            a dict with {id: obj} values.


    Note: in all instance methods, pass critical=True as a keyword argument to
    make any requests generated in that method critical, so that the script
    will exit (via logger.critical) if they fail.
    """

    def __init__(self, access_key='qstools', live=True):
        self._access_key = access_key
        self.live = live

        self.schoolcode = None
        self.api_key = None
        self.cache = QSAPICache()

        self._parse_access_key()

    # ============
    # = Students =
    # ============

    def get_students(self, show_deleted=False, show_has_left=False, **kwargs):
        """GET a list of all enrolled students from /students.

        If the student list is empty, [] will be returned.

        Args:
            by_id: Return a dict where the student ids are the keys.
            use_cache: Use the cache if it's available.
            class_id: Pull students from a specific class. This students will
                also be added to the cache along with all the students
                avaialable from /students.
            fields: A list of the extra fields to retrieve
        """
        if show_deleted or show_has_left:
            request = QSRequest(
                'GET all students, including deleted/has left',
                '/students')
            request.params.update({
                'showDeleted': show_deleted,
                'showHasLeft': show_has_left,
            })
            students = self.make_request(request, **kwargs)
            if 'by_id' in kwargs and kwargs['by_id'] is True:
                students = {i['id']: i for i in students}
            return students
        elif _should_make_request(self.cache.students, **kwargs):
            request = QSRequest('GET all students', '/students')
            students = self.make_request(request, **kwargs)
            self.cache.students.add(students)
        return self.cache.students.get(**kwargs)

    def get_student(self, student_id, use_cache=True, **kwargs):
        """GET a specific student by id. Returns None if no student is found.
        """
        cached = self.get_students(by_id=True, **kwargs).get(student_id)
        if cached:
            return cached
        else:
            request = QSRequest(
            'GET student by ID',
            '/students/{}'.format(student_id))
            return self.make_request(request, **kwargs)

    # =================
    # = Other Methods =
    # =================

    def make_request(self, request, **kwargs):
        """Process any QSRequest in this class and make it.

        Args:
            request: the prepared (but not yet made) QSRequest
            original_kwargs: the **kwargs passed to the function that
                instantiated this request, such as self.get_students().
        Returns:
            the data from the completed
        """
        request.set_api_key(self.api_key)
        if 'critical' in kwargs:
            request.critical = kwargs['critical']

        if 'fields' in kwargs:
            fields = kwargs['fields']
            if str(fields) == fields:
                fields = [fields]
            request.fields += fields

        request.make_request()

        if request.successful:
            qs.api_keys.set(self._api_key_store_key_path(), self.api_key)
        return request.data

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


class QSAPICache(object):
    """Essentially a wrapper around a bunch of RestCache objects."""

    def __init__(self):
        self.students = qs.ListWithIDCache(sort_key='fullName')


def _should_make_request(cache, **kwargs):
    if cache.get() is None:
        return True
    elif 'no_cache' in kwargs and kwargs['no_cache'] is True:
        return True
    elif 'fields' in kwargs and not cache.has_fields(kwargs['fields']):
        return True
    return False
