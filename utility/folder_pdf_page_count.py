#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Utility script to analyze page count in report cards in the current dir.

This counts the number of pages in each RC and compares to the target length.
For schools where the number of pages is important, this is a great way to
get an overview of what changes need to be made.

Searches the current directory (non recursively) for PDF's and counts their
pages.

CLI Usage:
folder_pdf_page_count.py {schoolcode} {target_length}

The target length is how long we *want* the PDF's to be.
"""

import re
import sys
import os
import json
import qs

_length_re = None
_api = None


def main():
    unordered = [ReportCard(i) for i in get_filenames()]
    ordered_cards = sorted(unordered, key=lambda x: x.length)

    short_cards = too_short(ordered_cards)
    long_cards = too_long(ordered_cards)
    right_cards = just_right(ordered_cards)

    qs.print_break()
    print "{} too short:".format(len(short_cards))
    print '\n'.join([str(i) for i in short_cards])
    qs.print_break()

    print "{} too long:".format(len(long_cards))
    print '\n'.join([str(i) for i in long_cards])
    qs.print_break()

    print "{} just right".format(len(right_cards))
    qs.print_break()


def too_short(cards):
    return [i for i in cards if i.length() < target_length()]


def too_long(cards):
    return [i for i in cards if i.length() > target_length()]


def just_right(cards):
    return [i for i in cards if i.length() == target_length()]


def get_filenames():
    for root, dirs, files in os.walk(os.curdir):
        return [i for i in files if os.path.splitext(i)[1] == '.pdf']


def target_length():
    return float(sys.argv[2])


def length_re():
    global _length_re
    if not _length_re:
        re_str = r"/Type\s*/Page([^s]|$)"
        _length_re = re.compile(re_str, re.MULTILINE | re.DOTALL)
    return _length_re


def api():
    global _api
    if not _api:
        _api = qs.API(sys.argv[1])
    return _api


class ReportCard(object):
    def __init__(self, filename):
        self.filename = filename

        self.student_name = os.path.splitext(self.filename)[0]
        self.student_name = self.student_name.split(' - ')[1]
        self.student_name = qs.unicode_decode(self.student_name)

    def __str__(self):
        return "{} ({}): {} pp".format(
            self.student_name,
            self.student_class_name(),
            self.length())

    def length(self):
        data = file(self.filename, 'rb').read()
        return len(length_re().findall(data))

    def student_class_name(self):
        student = api().get_students_by_name(self.student_name, silent=True)[0]
        return student['className']


if __name__ == '__main__':
    main()
