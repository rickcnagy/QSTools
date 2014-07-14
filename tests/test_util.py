"""Test the util module"""

import qs
import json

def test_dumps():
    complex_obj = [3, {1: [4, 5], 2: 2}, '5']
    assert json.dumps(complex_obj, indent=4) == qs.dumps(complex_obj)
    simple_obj = [{2: 1}, 5]
    simple_obj_json = '[\n    {\n        "2": 1\n    }, \n    5\n]'
    assert simple_obj_json == qs.dumps(simple_obj)
