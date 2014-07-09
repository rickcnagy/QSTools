#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Utility functions for inclusion in public QS package API"""

import json


def dumps(arbitry_obj):
    return json.dumps(arbitry_obj, indent=4)
