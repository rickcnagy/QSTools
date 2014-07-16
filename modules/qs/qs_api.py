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
        self.cache = QSCache()

        self._parse_access_key()

    # ============
    # = Students =
    # ============

    def get_students(self, by_id=False, use_cache=True, **kwargs):
        """GET a list of all enrolled students from /students.

        If the student list is empty, [] will be returned.

        Args:
            by_id: Return a dict where the student ids are the keys.
            use_cache: Use the cache if it's available.
            class_id: Pull students from a specific class. This students will
                also be added to the cache along with all the students
                avaialable from /students.
        """
        if self.cache.students is None or use_cache is False:
            request = QSRequest('GET all students', '/students')
            students = self.make_request(request, kwargs)
            self.cache.add_students(students)
        return self.cache.students_by_id() if by_id else self.cache.students

    def get_student(self, student_id, **kwargs):
        """GET a specific student by id. Returns None if the student isn't
        found.
        """
        student_id = qs.clean_id(student_id)
        student = self.get_students(by_id=True).get(student_id)
        if student:
            return student
        else:
            request = QSRequest(
                'GET student by ID',
                '/students/{}'.format(student_id))
            student = self.make_request(request, kwargs)
            return student if student else None

    # =================
    # = Other Methods =
    # =================

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


class QSCache(object):
    """Class for caching responses in a QSAPIWrapper object"""

    def __init__(self):
        self._students = {}

    # ============
    # = Students =
    # ============

    @property
    def students(self):
        """The cache for the /students URI. Returns an alphabetized list.

        Stored as a dictionary to avoid duplicating entries.
        """
        if self._students:
            return sorted(
                [v for k, v in self._students.iteritems()],
                key=lambda x: x['fullName'])

    def add_students(self, new_students):
        """Add students to the students cache.

        Each student gets a _cached key that is True

        Args:
            new_students: The new students to add. Must be a list.
        Raises:
            TypeError: new_students must be a list.
        """
        if type(new_students) is not list:
            raise TypeError('new_students must be a list, is {}'.format(
                type(new_students)))
        if not all(type(i) is dict for i in new_students):
            raise TypeError('new_students must contain only dicts')
        self._students.update({i['id']: i for i in new_students})

    def student(self, student_id):
        """Get a specific student by id"""
        return self._students.get(student_id)

    def students_by_id(self):
        """Get all the students in a dict like {studentID: student}"""
        return self._students
