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
    assert_in('sectionId', q.get_assignments(SECTION_WITH_GB)[0])


def test_get_final_grade():
    assignments = q.get_assignments(
        SECTION_WITH_GB,
        by_id=True,
        include_final_grades=True)
    assert_in(FINAL_GRADE_ID, assignments)
    assert_equals(assignments[FINAL_GRADE_ID]['name'], 'Final Grade')


def test_get_assignment():
    assignment = q.get_assignment(ASSIGNMENT_ID)
    assert_equals(assignment['name'], ASSIGNMENT_NAME)

    other_cache = qs.API()
    assignment = other_cache.get_assignment(ASSIGNMENT_ID)
    assert_equals(assignment['name'], ASSIGNMENT_NAME)
    assert_in('sectionId', assignment)


def test_with_grades():
    assignments = q.get_assignments(
        SECTION_WITH_GB,
        include_grades=True,
        by_id=True)
    assignment = assignments[ASSIGNMENT_ID]
    assert_in('grades', assignment)
    grades = assignment['grades']
    found_student = False
    for grade in grades:
        if grade['studentId'] == STUDENT_ID:
            assert_equals(grade['marks'], MARKS)
            found_student = True
        assert_equals(grade['assignmentId'], ASSIGNMENT_ID)
    assert_true(found_student)


def test_get_assignment_including_grades():
    with assert_raises(TypeError):
        q.get_assignment(ASSIGNMENT_ID, include_grades=True)
