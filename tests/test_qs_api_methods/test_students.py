"""Test the get_students() method"""

import qs
from nose.tools import *
from qs.test_data import *


def setup(module):
    global q, mock_student, test_student
    q = qs.API()
    q.get_students()
    mock_student = STUDENT
    test_student = q.get_students()[0]

# ===================
# = .get_students() =
# ===================


def test_get_students():
    students = q.get_students()

    assert_is_instance(students, list)
    assert_greater(len(students), 0)
    assert_equals(len(students), STUDENT_COUNT)

    api_mock_student = q.get_students(by_id=True)[mock_student['id']]
    assert_equals(api_mock_student['fullName'], mock_student['fullName'])


def test_get_students_by_id():
    by_id = q.get_students(by_id=True)
    assert_is_instance(by_id, dict)
    assert_greater(len(by_id), 0)
    assert_is_instance(by_id[by_id.keys()[0]], dict)
    assert_in('id', by_id[by_id.keys()[0]])


def test_get_deleted_students():
    students = q.get_students(show_deleted=True, by_id=True)
    assert_is_instance(students, dict)
    assert_in(DELETED_STUDENT_ID, students)
    assert_not_in(DELETED_STUDENT_ID, q.get_students(by_id=True))

# ==================
# = .get_student() =
# ==================


def test_get_student_for_valid_id():
    assert_equals(test_student, q.get_student(test_student['id']))


def test_get_student_for_invalid_id():
    assert_is_none(q.get_student(1))


def test_get_student_for_deleted_student():
    """Won't be in the cache"""
    student = q.get_student(DELETED_STUDENT_ID)
    assert_is_instance(student, dict)
    assert_greater(len(student), 0)
    assert_in('id', student)
    assert_equals(student['id'], DELETED_STUDENT_ID)
