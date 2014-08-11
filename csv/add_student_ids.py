#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Add a Student ID to each student row based on the First and Last columns.

Usage:
    ./add_student_id {filename.csv} {schoolcode}

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
    students = qs.CSV(filename)
    q = qs.API(schoolcode)

    for student in students:
        name = '{}, {}'.format(student['Last'], student['First'])
        by_name = {i['fullName']: i for i in q.get_students()}
        student['Student ID'] = by_name[name]['id']
    students.save("with student IDs")


if __name__ == '__main__':
    main()
