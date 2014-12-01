#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Utility script to analyze page count in report cards.

This counts the number of pages in each RC and compares to the target length.
For schools where the number of pages is important, this is a great way to
get an overview of what changes need to be made.

Searches the current directory (non recursively) for PDF's and counts their
pages.

CLI Usage:
folder_pdf_page_count.py {schoolcode}

If schoolcode is supplied (optional), then each student's class will be printed
along with their name
"""

import re
import os
import json
import qs

TARGET_LENGTH = 4


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
    return [i for i in cards if i.length() < 4]


def too_long(cards):
    return [i for i in cards if i.length() > 4]


def just_right(cards):
    return [i for i in cards if i.length() == 4]


def get_filenames():
    for root, dirs, files in os.walk(os.curdir):
        return [i for i in files if os.path.splitext(i)[1] == '.pdf']


class ReportCard(object):
    length_re =  re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE | re.DOTALL)

    # TODO: make schoolcode cli and optional
    # qs_api = qs.API('SCHOOLCODE')
    # qs.logger.silence()
    # qs_api.get_students(silent=True)

    def __init__(self, filename):
        self.filename = filename

        self.student_name = os.path.splitext(self.filename)[0]
        self.student_name = self.student_name.split(' - ')[1]

    def __str__(self):
        return "{} ({}): {} pp".format(
            self.student_name,
            self.student_class_name(),
            self.length())

    def length(self):
        data = file(self.filename, 'rb').read()
        return len(self.length_re.findall(data))

    def student_class_name(self):
        student = self.qs_api.get_students_by_name(self.student_name)[0]
        return student['className']


if __name__ == '__main__':
    main()
