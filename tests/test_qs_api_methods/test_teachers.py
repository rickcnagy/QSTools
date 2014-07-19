"""Test the methods for the /teachers endpoint"""

from nose.tools import *
import qs
from qs.test_data import *


def setup():
    global q
    q = qs.API()
    q.get_teachers()


def test_get_teachers():
    teachers = q.get_teachers()

    assert_is_instance(teachers, list)
    assert_equals(len(teachers), TEACHER_COUNT)
    assert_is_the_mock_teacher(q.get_teachers(by_id=True)[TEACHER_ID])


def test_get_teacher():
    assert_is_the_mock_teacher(q.get_teacher(TEACHER_ID))


def assert_is_the_mock_teacher(teacher):
    assert_equals(teacher['fullName'], TEACHER_NAME)
