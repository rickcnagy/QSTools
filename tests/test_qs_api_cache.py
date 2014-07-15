"""Test the QSCache class."""

import qs
from nose.tools import *

dummy_students = [
    {
        'id': '1234',
        'fullName': '02'
    }, {
        'id': '2345',
        'fullName': '04',
    }, {
        'id': '3456',
        'fullName': '01',
    }, {
        'id': '4567',
        'fullName': '02'
    }
]


def setup(module):
    global cache
    cache = qs.QSCache()


def test_get_empty_student_list():
    assert_is_none(cache.students)


def test_add_students():
    cache.add_students(dummy_students)


def test_add_single_student():
    with assert_raises(TypeError):
        cache.add_students(dummy_students[3])


def test_add_bad_list():
    with assert_raises(TypeError):
        cache.add_students(['hi', 'bye'])


def test_get_students():
    assert_is_instance(cache.students, list)
    assert_equals(len(cache.students), 4)
    assert_not_equal(dummy_students, cache.students)    # sorting
    sorted_dummy = sorted(dummy_students, key=lambda x: x['fullName'])
    assert_equal(sorted_dummy, cache.students)
