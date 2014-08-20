#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Add a Student ID to each student row based on the First and Last or Full
Name columns.

If ignore_case is true, this will ignore case when matching student names

Usage:
    ./add_student_id {filename.csv} {schoolcode} {ignore_case}

Requires:
    A CSV with "First" and "Last" columns, with an exact name match to the
        provided school database for each student.

Outputs:
    The same CSV, but with a "Student ID" column.
"""

import sys
import qs


def main():
    filename = sys.argv[1]
    schoolcode = sys.argv[2]
    ignore_case = bool(sys.argv[3]) if len(sys.argv) > 3 else True
    students = qs.CSV(filename)
    q = qs.API(schoolcode)

    by_name = {i['fullName']: i for i in q.get_students()}
    if len(by_name) != len(q.get_students()):
        qs.logger.critical('Student names are not unique in DB')
    else:
        qs.logger.info('Student names are unique.')
    student_names_not_matched = set()
    for student in students:
        if 'Full Name' in student:
            full_name = student['Full Name']
        else:
            full_name = '{}, {}'.format(student['Last'], student['First'])

        if ignore_case is True:
            by_name = {k.lower(): d for k, d in by_name.iteritems()}
            full_name = full_name.lower()

        match = by_name.get(full_name)
        if match is None:
            if ignore_case:
                full_name = qs.tc(full_name)
            student_names_not_matched.add(full_name)
        else:
            student['Student ID'] = match['id']
    if student_names_not_matched:
        qs.logger.warning(
            'Some students in the file were not found in the db',
            student_names_not_matched)
    students.save("with student IDs")


if __name__ == '__main__':
    main()
