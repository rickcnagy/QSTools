"""Test methods related to the /assignments endpoints."""

from nose.tools import *
import qs
from qs.test_data import *


def setup():
    global q
    q = qs.API()


def test_get_assignments():
    assignments = q.get_assignments(SECTION_WITH_GB, by_id=True)
    assert_equals(assignments[ASSIGNMENT_ID]['name'], ASSIGNMENT_NAME)


def test_get_final_grade():
    assignments = q.get_assignments(
        SECTION_WITH_GB,
        by_id=True,
        include_final_grades=True)
    assert_in(FINAL_GRADE_ID, assignments)
    assert_equals(assignments[FINAL_GRADE_ID]['name'], 'Final Grade')
