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


# def test_get_section_enrollment():
#     # active semester
#     assert_valid_enrollment(q.get_section_enrollment(SECTION_ID))
#
#     # non active semester
#     assert_valid_enrollment(q.get_section_enrollment(NAS1_SECTION_ID))



def assert_valid_enrollment(enrollment):
    ids = []
    for student in enrollment['students']:
        print student
        print
        ids.append(student['id'])
    return set(ids) == set(SECTION_ENROLLMENT)
