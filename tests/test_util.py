"""Test the util module"""

import qs
import json

def test_dumps():
    obj = [3, {1: [4, 5], 2: 2}, '5']
    assert json.dumps(obj, indent=4) == qs.util.dumps(obj)
