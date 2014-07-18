"""Test the get_student() method"""

import qs
from nose.tools import *


def setup():
    global q, test_student
    q = qs.API()
    test_student = q.get_students()[0]


def test_get_student_for_valid_id():
    assert_equals(test_student, q.get_student(test_student['id']))


def test_get_student_for_invalid_id():
    assert_is_none(q.get_student(1))


def test_get_student_for_deleted_student():
    """Won't be in the cache"""
    student = q.get_student(qs.mock_data.DELETED_STUDENT_ID)
    assert_is_instance(student, dict)
    assert_greater(len(student), 0)
    assert_in('id', student)
    assert_equals(student['id'], qs.mock_data.DELETED_STUDENT_ID)
