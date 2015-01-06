"""Test the util module"""

import os
import json
import random
import datetime
from nose.tools import *
import qs


def setup():
    global http
    http = qs.HTTPBinRequest('test request', '/status/418')
    http.make_request()
    open('._qstest.txt', 'w').close()
    open('._qstest(5).txt', 'w').close()


def test_dumps():
    complex_obj = [3, {1: [4, 5], 2: 2}, '5']
    assert_equals(json.dumps(complex_obj, indent=4), qs.dumps(complex_obj))
    simple_obj = [{2: 1}, 5]
    simple_obj_json = '[\n    {\n        "2": 1\n    }, \n    5\n]'
    simple_obj_json_sorted = '[\n    {\n        "2": 1\n    }, \n    5\n]'
    assert_equals(simple_obj_json_sorted, qs.dumps(simple_obj))
    assert_equals(simple_obj_json, qs.dumps(simple_obj, sort=False))


def assert_dumps_str():
    assert_equals(qs.dumps(str), '"<type \'str\'>"')


def test_dumps_with_http_response():
    assert_in('teapot', qs.dumps(http.response))


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
    good_inputs = [1234, u'1234', '1234', '1g5H6', 0]
    for good_input in good_inputs:
        assert_equals(str(good_input), qs.clean_id(good_input))


def test_valid_id():
    value_errors = [None, {}, '']
    for error in value_errors:
        with assert_raises(ValueError):
            qs.clean_id(error)

    type_errors = [45.6, ['SomeID']]
    for error in type_errors:
        with assert_raises(TypeError):
            qs.clean_id(error)
        assert_false(qs.is_valid_id(error, check_only=True, func_name='test'))


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


def test_phone_funcs():
    raw = '1234567890'
    formatted = '(123) 456-7890'
    assert_true(qs.valid_us_phone(raw))
    assert_equals(qs.format_phone(raw), formatted)


def test_digits():
    assert_equals(qs.digits(' 123dfs'), '123')


def test_titlcase():
    assert_equals(qs.tc('some string'), 'Some String')


def test_unique_path():
    assert_equals(qs.unique_path('._qstest.txt'), '._qstest(1).txt')
    assert_equals(qs.unique_path('._qstest(3).txt'), '._qstest(3).txt')
    assert_equals(qs.unique_path('._qstest(5).txt'), '._qstest(6).txt')
    assert_equals(
        qs.unique_path('._qstest.txt', suffix='suf'),
        '._qstestsuf(1).txt')
    assert_in('_qstest', qs.unique_path('._qstest.txt', use_random=True))


def test_finance_to_float():
    assert_equals(qs.finance_to_float('$100.07'), 100.07)


def test_find_dups_in_dict_list():
    dict_1 = {'id': 1}
    dict_2 = {'id': 1}
    dict_3 = {'id': 2}

    all_dicts = [dict_1, dict_2, dict_3]
    dups = [dict_1, dict_2]

    assert_equals(qs.find_dups_in_dict_list(all_dicts, 'id'), dups)


def test_to_bool():
    true_strings = ['y', 'yes', 't', 'true', '1', '10']
    false_strings = ['n', 'no', 'f', 'false', '0']
    for true_string in true_strings:
        assert_true(qs.to_bool(true_string))
    for false_string in false_strings:
        assert_false(qs.to_bool(false_string))
    with assert_raises(ValueError):
        qs.to_bool('notabool')


def test_hex_to_int():
    assert_equals(qs.hex_to_int('#ffffff'), 16777215)
    with assert_raises(ValueError):
        qs.hex_to_int('notahex')


def test_parse_datestring():
    test_date = datetime.datetime(2014, 10, 13)
    assert_equals(qs.parse_datestring('2014-10-13'), test_date)


def teardown():
    os.remove('._qstest.txt')
    os.remove('._qstest(5).txt')
