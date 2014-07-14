"""Test the util module"""

import qs
import json
import random

def test_dumps():
    complex_obj = [3, {1: [4, 5], 2: 2}, '5']
    assert json.dumps(complex_obj, indent=4) == qs.dumps(complex_obj)
    simple_obj = [{2: 1}, 5]
    simple_obj_json = '[\n    {\n        "2": 1\n    }, \n    5\n]'
    assert simple_obj_json == qs.dumps(simple_obj)


def test_rand_str_length():
    length = randint(5, 10)
    rand_str = qs.rand_str(length)
    assert len(rand_str) == length


def test_rand_str_chars():
    filtered = [i for i in rand_str if i.isalnum()]
    assert len(filtered) == length


def test_rand_str_randomness():
    assert qs.rand_str() != qs.rand_str()
