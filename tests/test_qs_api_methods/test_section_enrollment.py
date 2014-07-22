"""Test methods related to /sectionenrollment"""

from nose.tools import *
import qs
from qs.test_data import *


def setup():
    global q
    q = qs.API()
    q.get_section_enrollments()


def test_get_section_enrollments():
    enrollments = q.get_section_enrollments()

    assert_is_instance(enrollments, list)
    assert_equals(len(enrollments), len(q.get_sections()))
    assert_valid_enrollment(q.get_section_enrollments(by_id=True)[SECTION_ID])


def test_get_section_enrollment():
    assert_valid_enrollment(q.get_section_enrollment(SECTION_ID))
    assert_valid_enrollment(q.get_section_enrollment(NAS1_SECTION_ID))


def test_section_enrollments_using_get_section_kwargs():
    sections = q.get_section_enrollments(
        semester_id=NAS2_SEMESTER_ID,
        by_id=True)
    assert_in(NAS2_SECTION_ID, sections)


def assert_valid_enrollment(enrollment):
    ids = []
    for student in enrollment['students']:
        print student
        print
        ids.append(student['id'])
    return set(ids) == set(SECTION_ENROLLMENT)
