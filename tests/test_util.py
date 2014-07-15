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
    assert_equals(qs.merge([{1: 1}, {2: 2}, {3: 3}]), {1: 1, 2: 2, 3: 3})
