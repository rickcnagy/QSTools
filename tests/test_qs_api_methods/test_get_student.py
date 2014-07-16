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


def test_student_id_types():
    identifier = str(test_student['id'])
    assert_equals(q.get_student(identifier), q.get_student(int(identifier)))
    with assert_raises(TypeError):
        q.get_student([identifier])
    with assert_raises(TypeError):
        q.get_student('')
