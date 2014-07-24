"""Test methods related to the /grades endpoint"""

from nose.tools import *
import qs
from qs.test_data import *


def setup():
    global q
    q = qs.API()


def test_get_grades():
    grades = q.get_grades(SECTION_WITH_GB)
    for grade in grades:
        if (grade['studentId'] == STUDENT_IN_GB_SECTION
                and grade['assignmentId'] == ASSIGNMENT_ID):
            assert_equals(grade['marks'], MARKS)
            assert_equals(grade['sectionId'], SECTION_WITH_GB)
