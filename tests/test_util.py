"""Test the util module"""

import qs
import json
import random
from nose.tools import *

def test_dumps():
    complex_obj = [3, {1: [4, 5], 2: 2}, '5']
    assert_equals(json.dumps(complex_obj, indent=4), qs.dumps(complex_obj))
    simple_obj = [{2: 1}, 5]
    simple_obj_json = '[\n    {\n        "2": 1\n    }, \n    5\n]'
    assert_equals(simple_obj_json, qs.dumps(simple_obj))


def test_rand_str_length():
    length = random.randint(5, 10)
    rand_str = qs.rand_str(length)
    assert_equals(len(rand_str), length)


def test_rand_str_chars():
    filtered = [i for i in qs.rand_str() if i.isalnum()]
    assert_equals(len(filtered), len(qs.rand_str()))


def test_rand_str_randomness():
    assert_not_equal(qs.rand_str(), qs.rand_str())

def test_merge():
    assert_equals(qs.merge({1: 1}, {2: 2}, {3: 3}), {1: 1, 2: 2, 3: 3})


def test_clean_id():
    value_errors = [None, {}, '']
    for error in value_errors:
        with assert_raises(ValueError):
            qs.clean_id(error)

    type_errors = [45.6, ['SomeID']]
    for error in type_errors:
        with assert_raises(TypeError):
            qs.clean_id(error)

    good_inputs = [1234, u'1234', '1234', '1g5H6', 0]
    for good_input in good_inputs:
        assert_equals(str(good_input), qs.clean_id(good_input))


def test_clean_args():

    @qs.clean_arg
    def to_be_cleaned(some_id):
        return some_id

    assert_is_instance(to_be_cleaned(1234), str)


def test_can_sense_nosetests():
    assert_true(qs.running_from_test())


def test_dict_to_from_dict_list():
    dict_to_test = {1: {2: 3, 'id': 1}, 2: {3: 4, 'id': 2}}
    matching_list = [{2: 3, 'id': 1}, {3: 4, 'id': 2}]
    assert_equals(qs.dict_list_to_dict(matching_list), dict_to_test)
    assert_equals(qs.dict_to_dict_list(dict_to_test), matching_list)

    assert_equals(
        dict_to_test,
        qs.dict_list_to_dict(qs.dict_to_dict_list(dict_to_test)))


def test_make_id():
    assert_equals(qs.make_id('123'), '123')
    assert_equals(qs.make_id(123, '456', u'789'), '123:456:789')
    with assert_raises(TypeError):
        qs.make_id([1234])
