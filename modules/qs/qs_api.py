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
            a dict with {id: dict} values.


    Note: in all instance methods, pass critical=True as a keyword argument to
    make any requests generated in that method critical, so that the script
    will exit (via logger.critical) if they fail.
    """

    def __init__(self, access_key='qstools', live=True):
        self._access_key = access_key
        self.live = live

        self.schoolcode = None
        self.api_key = None
        self.cache = _ResponseCache()

        self._parse_access_key()

    # =====================
    # = Semesters & Years =
    # =====================

    def get_semesters(self, **kwargs):
        """GET all semesters from /semesters"""
        if _should_make_request(self.cache.semesters, **kwargs):
            request = QSRequest('GET all semesters', '/semesters')
            semesters = self._make_request(request, **kwargs)
            self.cache.semesters.add(semesters)
        return self.cache.semesters.get()

    def get_semester(self, semester_id, **kwargs):
        """GET a specific semester by id"""
        return self._make_single_request(
            semester_id,
            '/semesters',
            self.get_semesters,
            'GET semester by ID',
            **kwargs)

    def get_active_semester(self):
        """GET the active semester dict"""
        return [i for i in self.get_semesters() if i['isActive']][0]['id']

    def get_active_year_id(self):
        """GET the active year id"""
        return self.get_active_semester()['yearId']

    def get_semesters_from_year(self, year_id=None):
        """GET all semesters from a specific year. If year_id isn't specified,
        defaults to the current year.
        """
        year_id = year_id or self.get_active_year_id()
        return [i for i in self.get_semesters() if i['yearId'] == year_id]


    # ============
    # = Students =
    # ============

    def get_students(self, show_deleted=False, show_has_left=False, **kwargs):
        """GET a list of all enrolled students from /students.

        Args:
            show_deleted: Show deleted students
            show_has_left: Show students that have left
        """
        if show_deleted or show_has_left:
            request = QSRequest(
                'GET all students, including deleted/has left',
                '/students')
            request.params.update({
                'showDeleted': show_deleted,
                'showHasLeft': show_has_left,
            })
            students = self._make_request(request, **kwargs)
            if 'by_id' in kwargs and kwargs['by_id'] is True:
                students = {i['id']: i for i in students}
            return students
        elif _should_make_request(self.cache.students, **kwargs):
            request = QSRequest('GET all students', '/students')
            students = self._make_request(request, **kwargs)
            self.cache.students.add(students)
        return self.cache.students.get(**kwargs)

    def get_student(self, student_id, **kwargs):
        """GET a specific student by id."""
        return self._make_single_request(
            student_id,
            '/students',
            self.get_students,
            'GET student by id',
            **kwargs)

    # =================
    # = Other Methods =
    # =================

    def _make_request(self, request, **kwargs):
        """Process any QSRequest in this class and make it.

        Args:
            request: the prepared (but not yet made) QSRequest
            kwargs: the **kwargs passed to the function that
                instantiated this request, such as self.get_students().
        Returns:
            The data from the completed request
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


    def _make_single_request(self, identifier, base_uri, request_all_method,
        request_description, **kwargs):
        """Make a single request to a resource that has both a method to
        request all and a method to request a single resource.

        Resources are such as /students/{studentID}, the single version of
        /students.

        Args:
            identifier: The id to be passed to the API in the URL, such as
                the student id.
            base_uri: The base URI of the the resource, such as '/students'.
            request_all_method: The method used to request all of the resource,
                such as self.students.
            request_description: The description to include in the request,
                such as 'GET student by id'.
            kwargs: The kwargs from the source method.
        """
        resource_id = qs.clean_id(identifier)
        cached = request_all_method(by_id=True, **kwargs).get(identifier)

        if cached:
            return cached
        else:
            request = QSRequest(
                request_description,
                '{}/{}'.format(base_uri, identifier))
            return self._make_request(request, **kwargs)

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

    class _ResponseCache(object):
        """Holder for caches of all responses from the API."""

        def __init__(self):
            self.students = qs.ListWithIDCache(sort_key='fullName')
            self.semesters = qs.ListWithIDCache()


def _should_make_request(cache, **kwargs):
    if cache.get() is None:
        return True
    elif 'no_cache' in kwargs and kwargs['no_cache'] is True:
        return True
    elif 'fields' in kwargs and cache.has_fields(kwargs['fields']) is False:
        return True
    return False
