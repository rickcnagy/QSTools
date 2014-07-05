#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

# from tqdm: https://github.com/noamraph/tqdm

import time

start_time = None
total = None
n = 0


def update(number=None):
    global n
    n = number if number else n + 1
    print meter(n, total, time.time() - start_time)


def start(total_param):
    """start the clock for update()
    total_param can be int or list"""
    global start_time
    global total

    if type(total_param) is list:
        total_param = len(total_param)
    if type(total_param) is not int:
        sys.exit("bad total_param. Should be list or int.")

    start_time = time.time()
    total = total_param


def format_interval(t):
    mins, s = divmod(int(t), 60)
    h, m = divmod(mins, 60)
    if h:
        return '%d:%02d:%02d' % (h, m, s)
    else:
        return '%02d:%02d' % (m, s)


def meter(n, total, elapsed):
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
