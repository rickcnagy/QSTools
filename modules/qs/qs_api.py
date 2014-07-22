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
    """

    def __init__(self, access_key='qstools', live=True):
        self._access_key = access_key
        self.live = live

        self.teacher_cache = qs.ListWithIDCache(sort_key='fullName')
        self.semester_cache = qs.ListWithIDCache()
        self.student_cache = qs.ListWithIDCache(sort_key='fullName')
        self.section_cache = qs.ListWithIDCache(sort_key='sectionName')
        self.section_enrollment_cache = qs.ListWithIDCache()

        self.schoolcode = None
        self.api_key = None

        self._parse_access_key()

    # =====================
    # = Semesters & Years =
    # =====================

    def get_semesters(self, **kwargs):
        """GET all semesters from /semesters."""
        cache = self.semester_cache
        if _should_make_request(cache, **kwargs):
            request = QSRequest('GET all semesters', '/semesters')
            semesters = self._make_request(request, **kwargs)
            cache.add(semesters)
        return cache.get(**kwargs)

    def get_semester(self, semester_id, **kwargs):
        """GET a specific semester by id."""
        return self._make_single_request(
            semester_id,
            '/semesters',
            self.get_semesters,
            'GET semester by ID',
            **kwargs)

    def get_active_semester(self):
        """GET the active semester dict."""
        return [i for i in self.get_semesters() if i['isActive']][0]

    def get_active_semester_id(self):
        """GET the id of the active semester."""
        return self.get_active_semester()['id']

    def get_active_year_id(self):
        """GET the active year id."""
        return self.get_active_semester()['yearId']

    def get_semesters_from_year(self, year_id=None):
        """GET a list of all semesters from a specific year. If year_id isn't
        specified, defaults to the current year.
        """
        year_id = year_id or self.get_active_year_id()
        return [i for i in self.get_semesters() if i['yearId'] == year_id]

    # ============
    # = Teachers =
    # ============

    def get_teachers(self, **kwargs):
        """GET teachers via the /teachers endpoint."""
        cache = self.teacher_cache
        if _should_make_request(cache, **kwargs):
            request = QSRequest('GET teachers', '/teachers')
            cache.add(self._make_request(request, **kwargs))
        return cache.get(**kwargs)

    def get_teacher(self, teacher_id, **kwargs):
        """GET a specific teacher by id."""
        return self._make_single_request(
            teacher_id,
            '/teachers',
            self.get_teachers,
            'GET teacher by ID',
            **kwargs)

    # ============
    # = Students =
    # ============

    def get_students(self, show_deleted=False, show_has_left=False, **kwargs):
        """GET a list of all enrolled students from /students.

        Args:
            show_deleted: Show deleted students.
            show_has_left: Show students that have left.
        """
        cache = self.student_cache
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
        elif _should_make_request(cache, **kwargs):
            request = QSRequest('GET all students', '/students')
            students = self._make_request(request, **kwargs)
            cache.add(students)
        return cache.get(**kwargs)

    def get_student(self, student_id, **kwargs):
        """GET a specific student by id."""
        return self._make_single_request(
            student_id,
            '/students',
            self.get_students,
            'GET student by id',
            **kwargs)

    # ============
    # = Sections =
    # ============

    def get_sections(self, semester_id=None, all_semesters=False,
        active_only=True, **kwargs):
        """GET sections from the /sections endpoint.

        Args:
            semester_id: GET sections from a specific semester by id.
            all_semesters: GET sections from all semesters for this school.
                semester_id get priority over this.
            active_only: Only return sections from the current semester. If
                this is False, sections from all semesters already in the cache
                are returned, otherwise it's the active semester only.
                all_semesters and semester_id get priority.

        """
        cache = self.section_cache

        def mark_sections(sections, semester_id_to_mark):
            for section in sections:
                section.update({'semesterId': semester_id_to_mark})

        if semester_id:
            semester_id = qs.clean_id(semester_id)
            kwargs.update({'filter_dict': {'semesterId': semester_id}})

            if _should_make_request(cache, **kwargs):
                request = QSRequest('GET sections from semester', '/sections')
                request.params.update({'semesterId': semester_id})
                sections = self._make_request(request, **kwargs)
                mark_sections(sections, semester_id)
                cache.add(sections)

        elif _should_make_request(cache, **kwargs):
            request = QSRequest('GET sections', '/sections')
            sections = self._make_request(request, **kwargs)
            mark_sections(sections, self.get_active_semester_id())
            cache.add(sections)

        if all_semesters is True:
            active_only = False
            all_sections = []
            for semester in self.get_semesters():
                sections = self.get_sections(semester_id=semester['id'])
                all_sections.append(sections)

        if semester_id is None and active_only is True:
            semester_id_dict = {'semesterId': self.get_active_semester_id()}
            kwargs.update({'filter_dict': semester_id_dict})

        return cache.get(**kwargs)

    # =======================
    # = Section Enrollments =
    # =======================

    def get_section_enrollments(self, **kwargs):
        """GET section enrollments for the active semester.
        For speed, uses an extra field in the /students endpoint. Data is still
        stored in the cache by section id.

        Takes the sames kwargs as `.get_sections()` for deciding which
        sections to show.
        """
        self._update_section_enrollment_cache()
        by_id = kwargs.get('by_id')

        section_enrollment_kwargs = qs.merge(kwargs, {'by_id': False})
        section_kwargs = qs.merge(kwargs, {'by_id': True})
        all_enrollment = [
            self.get_section_enrollment(i)
            for i in self.get_sections(**section_kwargs)
        ]
        if by_id:
            return qs.dict_list_to_dict(all_enrollment)
        else:
            return all_enrollment

    def get_section_enrollment(self, section_id, **kwargs):
        """GET section enrollment for a specific section ID. Note that if the
        section is from a non-active semester, this is the only way to access
        that section's enrollment.
        """
        cache = self.section_enrollment_cache
        section_id = qs.clean_id(section_id)

        self._update_section_enrollment_cache()
        cached = cache.get(section_id, **kwargs)
        if cached:
            return cached
        else:
            request = QSRequest(
                'GET section enrollment for non-active section',
                '/sectionenrollments/{}'.format(section_id))
            students = self._make_request(request, **kwargs)['students']
            section_enrollments = {'id': section_id, 'students': []}
            section_enrollments['students'] = [
                self._enrollment_dict(i) for i in students
            ]
            cache.add(section_enrollments)
        return cache.get(section_id, **kwargs)

    def get_student_enrollments(self, **kwargs):
        """GET the section enrollment by student, for all students/sections.
        Accepts the same kwargs as `.get_sections()` for determining which
        sections to show.

        Returns: A dict, by student id, of all sections that student takes:
        `{studentID1: [sectionID1, sectionID2], 'studentID1': [...]}`
        """
        by_section = self.get_section_enrollments(**kwargs)
        if type(by_section) is list:
            by_section = qs.dict_list_to_dict(by_section)

        all_students = {}
        for section_id, student_list in by_section.iteritems():
            for student_id in [i['id'] for i in student_list['students']]:
                if student_id not in all_students:
                    all_students[student_id] = []
                all_students[student_id].append(section_id)
        return all_students

    def get_student_enrollment(self, student_id, **kwargs):
        """GET the sections a specific student is enrolled in, by ID.
        Accepts the same kwargs as `.get_sections()` for determining which
        sections to show.
        """
        return self.get_student_enrollments(**kwargs).get(student_id)

    # =============
    # = Protected =
    # =============

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
        request all and a method to request a single resource. Handles both
        the request part and caching part.

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
        cached = request_all_method(by_id=True, **kwargs).get(resource_id)

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

    def _enrollment_dict(self, student):
        student_id = student.get('id') or student.get('smsStudentStubId')
        return {
            'id': student_id,
            'smsStudentStubId': student_id,
            'fullName': student['fullName'],
        }

    def _update_section_enrollment_cache(self, **kwargs):
        """Update the section enrollments cache based on the /students
        endpoint. This only updates the cache for the current semester.
        """
        cache = self.section_enrollment_cache
        if _should_make_request(cache, **kwargs):
            students = self.get_students(fields='smsClassSubjectSetIdList')
            section_enrollments = {}
            for student in students:
                for section_id in student['smsClassSubjectSetIdList']:
                    if section_id not in section_enrollments:
                        section_enrollments[section_id] = []
                    section_enrollments[section_id].append(
                        self._enrollment_dict(student)
                    )
            enrollment_list = [
                {'id': k, 'students': v}
                for k, v in section_enrollments.iteritems()
            ]
            cache.add(enrollment_list)


def _should_make_request(cache, **kwargs):
    """Whether or not a new QS API request should be made, based on cache
    status and kwargs.
    """
    no_cache = kwargs.get('no_cache')
    fields = kwargs.get('fields')

    if no_cache is True:
        return True
    elif fields and cache.has_fields(fields) is False:
        return True
    elif cache.get(**kwargs) is None:
        return True
    return False
