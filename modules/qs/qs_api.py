#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""
various tools for working with the QuickSchools API
"""

import sys
import os
import json
import random
import requests
import time

# api key should be stored in separate file and pasted in
api_key = ''
use_live_server = True

WAIT_THRESHOLD = 5
WAIT_TIME = 1

base_uri = None
_error_count = 0
wait_count = 0

# API resources that don't (generally) change, so can be cached
sections = {}
enrollments = {}
report_cycles = None
semesters = None
students = None
teachers = None
recent_student_fields = None
enrollments_by_student = None

# =================
# = REST API calls
# ==================
"""All API functions return a dictionary or a list of dictionaries"""

# =============
# = Semesters =
# =============


def get_semesters(critical=False):
    global semesters
    if not semesters:
        r = QSRequest()
        r.uri = "/semesters"
        r.description = "GET all semesters"
        r.critical = critical
        r.make_request()
        semesters = r.data
    return semesters


def get_semester(semester_id, critical=False):
    r = QSRequest()
    r.uri = "/semesters/{}".format(semester_id)
    r.description = "GET semester"
    r.critical = critical
    r.make_request()

    return r.data


def get_semesters_from_year(year_id=None):
    """GET semester objs only from a given year

    Args:
        year_id: the year id to filter on. Defaults to the current year.

    Returns:
        A list of semester objs from the given year.
    """
    year_id = year_id or get_active_semester()['yearId']
    return [
        i for i in get_semesters()
        if i['yearId'] == year_id
    ]


def get_active_semester(critical=False):
    """GET the active semester.
    Note that this also gives the active year with yearName and yearId
    """
    semesters = get_semesters(critical)
    return [i for i in semesters if i['isActive']][0]

# ============
# = Students =
# ============


def get_students(fields=None, critical=False):
    global students
    if not students or recent_student_fields != fields:
        r = QSRequest()
        r.uri = "/students"
        r.description = "GET all students"
        if fields:
            r.description += " with additional fields"
            r.params = {"fields": fields}
        r.critical = critical
        r.make_request()
        students = r.data
    return students


def get_student(student_id, critical=False):
    """Get student data by id, mostly cached.
    If id isn't in students cache, then get student and add them to the cache.
    """
    global students
    students_by_id = {i['id']: i for i in get_students(critical=critical)}
    if student_id in students_by_id:
        return students_by_id[student_id]
    else:
        r = QSRequest()
        r.uri = '/students/{}'.format(student_id)
        r.description = "GET specific student"
        r.params = {'showDeleted': 'true', 'showHasLeft': 'true'}
        r.critical = critical
        r.make_request()
        students.append(r.data)
        return r.data

# ============
# = Teachers =
# ============


def get_teachers(fields=None, critical=False):
    global teachers
    if not teachers:
        r = QSRequest()
        r.uri = "/teachers"
        r.description = "GET all teachers"
        if fields:
            r.description += " with additional fields"
            r.params = {"fields": fields}
        r.critical = critical
        r.make_request()
        teachers = r.data
    return teachers


# ============
# = Sections =
# ============


def get_sections(semester_id='current', update_cache=False, critical=False):
    """GET all sections in semester_id. Repeated responses are cached by semester id.

    Args:
        semester_id: The semester id to GET from. Default is the current semester.
        update_cache: Ignore cache for semester id and make new response and then update cache
    """
    global sections

    cached = sections.get(semester_id)
    if update_cache or cached is None:
        r = QSRequest()
        r.uri = "/sections"
        r.description = "GET all sections"
        r.critical = critical
        if semester_id != 'current':
            r.params['semesterId'] = semester_id
        r.params['fields'] = 'smsAcademicSemesterId,smsClassId'
        r.make_request()
        sections[semester_id] = r.data
        return r.data
    else:
        return cached


def get_all_section_ids(semester_id=None, critical=False):
    sections = get_all_sections(semester_id)

    section_ids = []
    for section in sections:
        section_ids.append(section['id'])

    return section_ids


def get_section(section_id, critical=False):
    """GET a specific section. Cached almost all of the time.
    If a section isn't already in the cache, then find its semester_id
    and add that entire semester to the cache. This updates the module-wide
    'semesters' cache object.
    """
    all_cached_sections = []
    for k, v in sections.iteritems():
        all_cached_sections += v
    cached_sections_by_id = {i['id']: i for i in all_cached_sections}

    if section_id in cached_sections_by_id:
        return cached_sections_by_id[section_id]
    else:
        r = QSRequest()
        r.description = "GET section"
        r.uri = "/sections/{}".format(section_id)
        r.params = {'fields': 'smsAcademicSemesterId,smsClassId'}
        r.critical = critical
        r.make_request()

        # for cache
        get_sections(semester_id=r.data['smsAcademicSemesterId'])
        return r.data

# =======================
# = Section Enrollments =
# =======================


def get_enrollment(section_id, update_cache=False, critical=False):
    # TODO: use get_enrollments_by_student and transform to be by section instead of 1 request per section
    cached = enrollments.get(section_id)
    if update_cache or cached is None:
        r = QSRequest()
        r.description = "GET section enrollments"
        r.uri = "/sectionenrollments/{}".format(section_id)
        r.critical = critical
        r.make_request()

        # Assembla #2164
        for d in r.data['students']:
            d['id'] = d['smsStudentStubId']

        enrollments[section_id] = r.data
        return r.data
    else:
        return cached


def get_enrollments_by_student(critical=False):
    """GET sections enollments by student. Cached for performance.

    Returns:
        Dict with key as student id, list of ids as values:
        {studentID1: [sectionID1, sectionID2], 'studentID1': [...]}
    """
    if enrollments_by_student is None:
        r = QSRequest()
        r.description = "GET section enrollment by student"
        r.uri = '/students'
        r.critical = critical
        r.params = {'fields': 'smsClassSubjectSetIdList'}
        r.make_request()
        enrollments_by_student = {
            i['id']: i['smsClassSubjectSetIdList'] for i
            in r.data
        }
    return enrollments_by_student


# ===============
# = Assignments =
# ===============


def get_assignments(section_id, include_final_grades=None, critical=False):
    r = QSRequest()
    r.description = "GET assignments"
    r.uri = "/sections/{}/assignments".format(section_id)
    if (include_final_grades):
        r.params = {'includeFinalGrades': include_final_grades}
    r.critical = critical
    r.make_request()

    for assignment in r.data:
        assignment['sectionId'] = section_id
    return r.data


def post_assignment(section_id, assignment, critical=False):
    """assignment is dict, supports all the fields at apidocs.quickschools.com/#assignment"""
    r = QSRequest()
    r.function = requests.post
    r.description = "POST assignment"
    r.uri = "/sections/{}/assignments".format(section_id)
    r.critical = critical
    r.params = assignment
    r.make_request()

    return r.data


def delete_assignment(section_id, assignment_id, critical=False):
    r = QSRequest()
    r.function = requests.delete
    r.description = "DELETE assignment"
    r.uri = "/sections/{}/assignments/{}".format(section_id, assignment_id)
    r.critical = critical
    r.make_request()

    return r.data

# ==========
# = Grades =
# ==========


def get_grades(section_id, assignment_id, critical=False):
    r = QSRequest()
    r.description = "GET grades"
    r.uri = "/grades"
    r.params = {'sectionId': section_id, 'assignmentId': assignment_id}
    r.critical = critical
    r.make_request()

    return r.data


def post_grades(section_id, assignment_id, grades, critical=False):
    """grades is list formatted like at apidocs.quickschools.com/#grades"""
    r = QSRequest()
    r.function = requests.post
    r.description = "POST grades"
    r.uri = "/grades"
    r.critical = critical
    if type(grades) is not str:
        grades = json.dumps(grades)
    r.params = {
        'sectionId': section_id, 'assignmentId': assignment_id,
        'grades': grades
    }
    r.make_request()

    return r.data

# ================
# = Report Cards =
# ================


def get_report_cycles(critical=False):
    """GET all report cycles. Cached."""
    global report_cycles
    if not report_cycles:
        r = QSRequest()
        r.description = "GET all report cycles"
        r.uri = '/reportcycles'
        r.critical = critical
        r.make_request()
        report_cycles = r.data
    return report_cycles


def get_active_report_cycle():
    return [i for i in get_report_cycles() if i['isActive']][0]


def get_report_card_data(student_id, report_cycle_id=None, critical=False):
    """GET report card data by student and report cycle id.
    Requests ALL identifiers, so slow: ~1s.

    Args:
        reportcycle_id: if None is specified, uses active report cycle
    """
    report_cycle_id = report_cycle_id or get_active_report_cycle()

    r = QSRequest()
    r.description = "GET report card data"
    r.uri = '/students/{}/reportcards/{}'.format(student_id, report_cycle_id)
    r.critical = critical
    r.make_request()
    return r.data

# ===============
# = Transcripts =
# ===============

def get_transcript(student_id, critical=False):
    """GET transcript data for student_id."""
    r = QSRequest()
    r.description = 'GET transcript data'
    r.uri = '/transcripts/{}'.format(student_id)
    r.critical = critical
    r.make_request()
    return r.data


def post_transcript(student_id, transcript_level={}, semester_level={}, section_level={}, critical=False):
    """POST transcript data by student.
    transcript_level, semester_level, or section_level must be not empty.

    Args:
        student_id: student id to upload to

        transcript_level: transcript level identifiers and values formatted like so:

        {'values': {'identifer1': 'value1', 'identifier2: '...'}}

        semester_level: semester level identifiers, format:

        {'semesterId1': {'values': {'identifier1': 'value1', 'identifier2': ...}}, 'semesterId2': ...}

        section_level: same, but for section level identifiers. Replace semesterId with sectionId.
    """
    r = QSRequest()
    r.description = 'POST transcript data'
    r.uri = '/transcripts/{}'.format(student_id)
    r.function = requests.post
    r.critical = critical
    r.request_data = {
        'transcriptLevel': json.dumps(transcript_level),
        'semesterLevel': json.dumps(semester_level),
        'sectionLevel': json.dumps(section_level),
    }
    r.make_request()
    return r.data

# =======================================
# = Utility functions related to QS API =
# =======================================


def get_error_count():
    return _error_count


def get_schoolcode():
    return api_key[:api_key.find('.')]


def get_base_uri():
    global base_uri
    return 'https://api.quickschools.com/sms/v1'
    if not base_uri:
        if use_live_server:
            base_uri = 'https://api.quickschools.com/sms/v1'
        else:
            base_uri = 'https://api.smartschoolcentral.com/sms/v1'
    return base_uri


def student_ids_to_names(student_ids):
    students_by_id = {i['id']: i for i in get_students()}
    return [students_by_id[i]['fullName'] for i in student_ids]


def cd():
    """either cd into school's path or create it; schema: /script/schoolcode"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    school_path = os.path.dirname(os.path.abspath(__file__)) + "/" + get_schoolcode()
    if not os.path.exists(school_path):
        os.makedirs(school_path)
    os.chdir(school_path)


def wait():
    global wait_count
    if use_live_server:
        wait_count += 1
        if not wait_count % WAIT_THRESHOLD:
            time.sleep(WAIT_TIME)


def pprint(data):
    """Pretty-print data for terminal output, etc. Uses JSON.dumps().

    Args:
        data: any arbitrary data construct
    """
    print json.dumps(data, indent=4)

# =================================================
# = Functions to match sections between semesters =
# =================================================


def match_section_by_id(match_section_id, match_teacher=True, semester_id=None, source_semester_cache=None):
    """Get the matching section from in target (usually current)
    semester based on section_id arg

    Args:
        source_semester_cache: cache requests by passing in previous response from get_section.
                Do this if making repeated checks and get_sections(semester_id=xxx) isn't changing
    """

    if source_semester_cache:
        match_section = {
            i['id']: i
            for i
            in source_semester_cache
        }[match_section_id]
    else:
        match_section = get_section(match_section_id)
    return match_section_by_dict(match_section, match_teacher=match_teacher, semester_id=semester_id, section_id=match_section_id)


def match_section_by_dict(section_dict, match_teacher=True, semester_id=None, section_id=None):
    """section_obj is a dict (such as returned from get_section())
    with fields for section matching the published API fields.
    Section_id arg is just for helpful log message
    """
    section_name = section_dict['sectionName'].strip()
    class_name = section_dict['className'].strip()
    code = section_dict['sectionCode'].strip()
    teacher_id = None
    if match_teacher and len(section_dict['teachers']):
        teacher_id = section_dict['teachers'][0]['id']
    return match_section_by_info(
        section_name=section_name,
        class_name=class_name,
        section_code=code,
        teacher_id=teacher_id,
        semester_id=semester_id,
        section_id=section_id)


def match_section_by_name(section_name, semester_id=None):
    """Match sections by name - e.g. for report card matching"""
    return match_section_by_info(section_name=section_name, semester_id=semester_id)


def match_section_by_info(section_name=None, class_name=None, section_code=None, teacher_id=None, semester_id=None, section_id=None):
    """get the matching section from the current semester based on info args

    section_id arg is just for helpful log message
    """
    match = None
    error_text = ''

    def error(message):
        api_logging.error(message, {
            'Section name': section_name,
            'Class name': class_name,
            'Section code': section_code,
            'Teacher ID': teacher_id,
            'Section ID': section_id,
            'Found matches': found_matches
        })

    section_name = section_name.strip() if section_name else section_name
    class_name = class_name.strip() if class_name else class_name
    section_code = section_code.strip() if section_code else section_code

    found_matches = {
        i: False
        for i
        in ['Section Name', 'Class Name', 'Section Code', 'Teacher ID']
    }
    for candidate in get_sections(semester_id):
        cand_name = candidate['sectionName'].strip()
        cand_class = candidate['className'].strip()
        cand_code = candidate['sectionCode'].strip()
        cand_teacher_ids = [i['id'] for i in candidate['teachers']]

        if ((not section_name or section_name == cand_name)
                and (not class_name or class_name == cand_class)
                and (not section_code or section_code == cand_code)
                and (not teacher_id or teacher_id in cand_teacher_ids)):
            if match:
                error('multiple matches for subject')
                return
            match = candidate

        if section_name and section_name == cand_name:
            found_matches['Section Name'] = True
        if class_name and class_name == cand_class:
            found_matches['Class Name'] = True
        if section_code and section_code == cand_code:
            found_matches['Section Code'] = True
        if teacher_id and teacher_id in cand_teacher_ids:
            found_matches['Teacher ID'] = True
    if match:
        return match
    else:
        error("couldn't find match for subject")

# ==========================================================
# = Functions to check for discrepancies between semesters =
# ==========================================================


def sections_with_enrollment_discrepancies(source_semester, target_semester=None):
    """Gives a list of all sections in source with 1:1 enrollment correlation in target.
    Additional enrollments in target are ok.

    Args:
        source_semester: id of source semester
        target_semester: id of target semester. None=current semester.

    Returns:
        A list of all ids of sections in source with enrollment discrepencies
        If a section itself doesn't have a match in target, then it is included in this list
        Checking for enrollment also checks for sections

        Note that if it matches completely, [] is returned, which equates to None
    """
    matches = []
    mismatches, match_dict = section_discrepancies(source_semester, target_semester=target_semester)
    possible_matches = [
        i['id'] for i
        in get_sections(semester_id=source_semester)
        if i['id'] not in mismatches
    ]
    for section in possible_matches:
        if has_matching_enrollment(section, match_dict[section]['id']):
            matches.append(section)
        else:
            mismatches.append(section)
    return mismatches


def enrollment_discrepancies(source_section, target_section):
    source_enrollments = [
        i['id'] for i
        in get_enrollment(source_section)['students']
    ]
    target_enrollments = [
        i['id'] for i
        in get_enrollment(target_section)['students']
    ]
    return [i for i in source_enrollments if i not in target_enrollments]


def section_discrepancies(source_semester, target_semester=None):
    """Need 1:1 correlation for every section in source.
    Additional sections in target is ok.

    Args:
        source_semester: id of source semester
        target_semester: id of target semester. None=current semester.

    Returns:
        A *TUPLE* containing the ids without matches, and a dict mapping
        matching sections with their match, like so:
        ([123, 124], {12345: 123123})
    """
    mismatches = []
    matches = {}
    target_sections = get_sections(semester_id=target_semester)
    source_sections = get_sections(semester_id=source_semester)
    for section in source_sections:
        match = match_section_by_id(section['id'], semester_id=target_semester, source_semester_cache=source_sections)
        if match:
            matches[section['id']] = match
        else:
            mismatches.append(section['id'])
    return mismatches, matches


def has_matching_enrollment(source_section, target_section):
    """Check for whether the enrollment matches between sections.
    All of source's enrollments must be in target, but target may
    have additional enrollments not in source.
    Matching is done by section ID and student ID.

    Args:
        source_section: id of source section
        target_section: id of target section

    Returns:
        A boolean of whether or not there is a complete enrollment match
        between them
    """
    return enrollment_discrepancies(source_section, target_semester) == []


def has_matching_section(source_section, target_semester=None, match_teacher=False):
    """Check whether source_section has a match in target_semester.
    By default doesn't check for teacher match.

    Args:
        source_section: id of source section. Can be any semester.
        target_semester: id of target semester. None=current semester.

    Returns:
        A boolean of whether source_section has a match in target_semester
    """
    return match_section_by_id(
        source_section,
        semester_id=target_semester,
        match_teacher=match_teacher) is not None


# ===========
# = Classes =
# ===========


class QSRequest(object):
    """QSRequest class is for making requests via API"""

    def __init__(self):
        self.response = None
        self.uri = ''
        self.params = {}
        self.request_data = {}
        self.description = ''
        self.function = requests.get
        self.critical = False
        self.json = None
        self.data = None
        self.text = None

    def full_uri(self):
        return get_base_uri() + self.uri

    def full_params(self):
        standard_params = {'apiKey': api_key,
            'itemsPerPage': 1000,
            'URI': self.uri,
            'data': self.request_data,
        }
        return dict(standard_params.items() + self.params.items())

    def make_request(self):
        self.check_for_ready()
        api_logging.info(self.description, self.full_params(), False, is_request=True)
        self.response = self.function(
            self.full_uri(),
            params=self.full_params(),
            data=self.request_data)
        self.text = self.response.text
        self.json = self.response.json()
        self.process_response()
        self.set_data()
        wait()
        return self.data

    def process_response(self):
        global _error_count

        output = self.description
        if self.success():
            api_logging.info(self.description, self.json, True)
        else:
            _error_count += 1
            api_logging.error_or_critical(self.description, self.json, self.critical)

    def success(self):
        return self.response.status_code == 200

    def check_for_ready(self):
        if not self.uri or not self.function or not self.description:
            api_logging.critical(
                "\n\n***can't make request - missing variables***\n"
                "must set uri and function description to make request", {})

    def set_data(self):
        if not self.success():
            self.data = []
            return
        try:
            if type(self.json) is list:
                self.data = self.json
            elif type(self.json) is dict:
                if 'list' in self.json.keys():
                    self.data = self.json['list']
                elif 'id' in self.json.keys():
                    self.data = self.json
                elif 'success' in self.json.keys():
                    self.data = self.json
                else:
                    raise BadResponseError
            else:
                raise BadResponseError
        except BadResponseError:
            api_logging.critical("Unrecognized response data type", self.json)


class BadResponseError(Exception):
    pass


# init
cd()
get_base_uri()
