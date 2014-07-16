"""Test the get_students() method"""

import qs
from nose.tools import *


def setup(module):
    global q, mock_student
    q = qs.API()
    q.get_students()
    mock_student = qs.mock_data.STUDENT


def test_get_students():
    students = q.get_students()

    assert_is_instance(students, list)
    assert_equals(len(students), qs.mock_data.STUDENT_COUNT)

    api_mock_student = q.get_students(by_id=True)[mock_student['id']]
    assert_equals(api_mock_student['fullName'], mock_student['fullName'])


def test_get_student():
    student = q.get_student(mock_student['id'])
    assert_equals(student['fullName'], mock_student['fullName'])
    assert_greater(len(q.get_students(by_id=True)), 0)
    assert_equals(student, q.get_students(by_id=True)[mock_student['id']])


def test_get_students_by_id():
    by_id_from_api = q.get_students(by_id=True)
    assert_is_instance(by_id_from_api, dict)
    by_id = {i['id']: i for i in q.get_students()}
    assert_equals(by_id_from_api, by_id)
