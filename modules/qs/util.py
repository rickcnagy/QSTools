#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Utility functions for inclusion in public QS package API"""

import json
import sys
import time
import string
import random
import os


def dumps(arbitry_obj):
    return json.dumps(arbitry_obj, indent=4)


def pp(arbitry_obj):  # pragma: no cover
    """Like pprint.pprint"""
    print dumps(arbitry_obj) if arbitry_obj else str(arbitry_obj)


def print_break():  # pragma: no cover
    """Print a break that's the width of the terminal for grouping output info.
    """
    # From http://stackoverflow.com/a/943921/1628796
    columns = int(os.popen('stty size', 'r').read().split()[1])
    print
    print '*' * columns
    print


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
        raise TypeError('The id ({}) must be a string or int'.format(some_id))


def bar(iterable, desc='', total=None, leave=True, file=sys.stderr,
        mininterval=0.5, miniters=1):  # pragma: no cover
    """Status bar for iterables, using tqdm: github.com/noamraph/tqdm

    Get an iterable object, and return an iterator which acts exactly like the
        iterable, but prints a progress meter and updates it every time a value
        is requested.
        'desc' can contain a short string, describing the progress, that is
        added in the beginning of the line.
        'total' can give the number of expected iterations. If not given,
        len(iterable) is used if it is defined.
        'file' can be a file-like object to output the progress message to.
        If leave is False, tqdm deletes its traces from screen after it has
        finished iterating over all elements.
        If less than mininterval seconds or miniters iterations have passed
        since the last progress meter update, it is not updated again.
    """

    def format_interval(t):
        mins, s = divmod(int(t), 60)
        h, m = divmod(mins, 60)
        if h:
            return '%d:%02d:%02d' % (h, m, s)
        else:
            return '%02d:%02d' % (m, s)

    def format_meter(n, total, elapsed):
        # n - number of finished iterations
        # total - total number of iterations, or None
        # elapsed - number of seconds passed since start
        if n > total:
            total = None

        elapsed_str = format_interval(elapsed)
        rate = '%5.2f' % (n / elapsed) if elapsed else '?'

        if total:
            frac = float(n) / total

            N_BARS = 10
            bar_length = int(frac * N_BARS)
            bar = '#' * bar_length + '-' * (N_BARS - bar_length)

            percentage = '%3d%%' % (frac * 100)

            left_str = format_interval(elapsed / n * (total - n)) if n else '?'

            return '|%s| %d/%d %s [elapsed: %s left: %s, %s iters/sec]' % (
                bar, n, total, percentage, elapsed_str, left_str, rate)

        else:
            return '%d [elapsed: %s, %s iters/sec]' % (n, elapsed_str, rate)

    class StatusPrinter(object):

        def __init__(self, file):
            self.file = file
            self.last_printed_len = 0

        def print_status(self, s):
            status = '\r' + s + ' ' * max(self.last_printed_len - len(s), 0)
            self.file.write(status)
            self.file.flush()

    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            total = None

    prefix = desc + ': ' if desc else ''

    sp = StatusPrinter(file)
    sp.print_status(prefix + format_meter(0, total, 0))

    start_t = last_print_t = time.time()
    last_print_n = 0
    n = 0
    for obj in iterable:
        yield obj
        # Now the object was created and processed, so we can print the meter.
        n += 1
        if n - last_print_n >= miniters:
            # We check the counter first, to reduce the overhead of time.time()
            cur_t = time.time()
            if cur_t - last_print_t >= mininterval:
                status = prefix + format_meter(n, total, cur_t - start_t)
                sp.print_status(status)
                last_print_n = n
                last_print_t = cur_t

    if not leave:
        sp.print_status('')
        sys.stdout.write('\r')
    else:
        if last_print_n < n:
            cur_t = time.time()
            sp.print_status(prefix + format_meter(n, total, cur_t - start_t))
        file.write('\n')
