#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Data migration via the QuickSchools API - utility module."""

import qs
import json
import os
import random
import sys
from tqdm import tqdm

filename = None
existing_filename = None
FILE_EXTENSION = '.json'


def create_file(prefix='', existing_file=False):
    prefix += '_' if prefix else ''
    # there's already a file, so new name is prefix + old basename
    if existing_file:
        new_filename = '{}{}'.format(prefix, basename(get_existing_filename()))
    else:
        new_filename = '{}{}_{}'.format(
            prefix, qs.get_schoolcode(), str(random.randint(1, 100)))
    set_filename(new_filename + FILE_EXTENSION)
    return get_filename()

def load(prefix=''):
    prefix += '_' if prefix else ''
    old_fullname = prefix + basename(get_existing_filename()) + FILE_EXTENSION
    return json.load(open(old_fullname))


def save(data, log=True):
    json.dump(data, open(get_filename(), 'w'), indent=4)
    api_logging.info("dumped JSON data to file: " + get_filename(), data, cc_print=True)


def set_filename(new_filename):
    global filename
    filename = new_filename


def get_existing_filename():
    global existing_filename
    if not existing_filename:
        existing_filename = raw_input("Data filename?\n").strip("'")
    return existing_filename


def get_filename():
    return filename


def basename(long_name):
    basename = long_name
    if len(long_name.split('_')) > 2:
        basename = basename[basename.find('_') + 1:]
    return os.path.splitext(basename)[0]


def run_id():
    return get_filename()[-4:-2]


# confirm that everything's good before working with data
def check_before_run(compare_date=None):
    print compare_date
    server_warning = "**USING LIVE SERVER!**" if qs.use_live_server \
        else "using backup server"

    compare_date_warning = "Assignments on or after {}\n".format(compare_date) \
        if compare_date is not None else ''

    question = "Starting using following parameters:" if not qs.use_live_server \
        else "*Does this all look correct?** (type y for yes)"

    statement = ("\n{}\nSchoolcode: {}\n{}\n{}".format(
                question,
                qs.get_schoolcode(),
                server_warning,
                compare_date_warning))

    if (qs.use_live_server):
        if not confirm(statement=statement):
            sys.exit('user aborted')
    else:
        api_logging.info(statement, {}, cc_print=True)


def complete():
    api_logging.info("Complete. {} errors."
        .format(qs.get_error_count()),{}, cc_print=True)


def confirm(statement='Confirm before proceeding (y):'):
    """Confirm that the user is ok with what's happening before proceeding"""
    return raw_input(statement).lower() == 'y'


def indicator(iterable, description):
    """Wrapper around tqdm.

    Params:
        description: some meaningful description, such as 'GET'
    """
    return tqdm(iterable, desc=description, leave=True)
