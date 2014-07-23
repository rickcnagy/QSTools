#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Utility functions for inclusion in public QS package API"""

import json
import string
import random
import subprocess


def dumps(arbitry_obj):
    return json.dumps(arbitry_obj, indent=4)


def pp(arbitry_obj):  # pragma: no cover
    """Like pprint.pprint"""
    print dumps(arbitry_obj) if arbitry_obj else str(arbitry_obj)


def print_break():  # pragma: no cover
    """Print a break that's the width of the terminal for grouping output info.
    """
    columns = int(subprocess.check_output(['stty', 'size']).split()[1])
    print
    print '*' * columns
    print


def dict_list_to_dict(dict_list, id_key='id'):
    """Takes a list of dicts and flattens them to a single dict using the
    id_key for the keys in the flattened dict.
    """
    return {i[id_key]: i for i in dict_list}


def dict_to_dict_list(large_dict):
    """Takes a single dict and expands it out to a list of dicts."""
    return [v for k, v in large_dict.iteritems()]


def rand_str(size=6, chars=string.letters + string.digits):
    """http://stackoverflow.com/a/2257449/1628796"""
    return ''.join(random.choice(chars) for _ in range(size))


def merge(*args):
    """Returned merged version of indefinite number of dicts. Just like the
    builtin dict() method, args to right get precedent over args to the left.

    Example usage: qs.merge({1: 2}, {3: 4}).
    """
    merged = []
    for unmerged in args:
        for item in unmerged.items():
            merged.append(item)
    return dict(merged)

merge({1: 2}, {3: 4})


def running_from_test():
    """Tell whether the current script is being run from a test"""
    return 'nosetests' in sys.argv[0]


def clean_id(some_id):
    if not some_id and some_id != 0:
        raise ValueError('The id must not be none')
    elif type(some_id) is int or str(some_id) == some_id:
        return str(some_id)
    else:

