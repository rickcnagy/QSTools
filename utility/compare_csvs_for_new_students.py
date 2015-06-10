"""
Compare CSV for New Students

This script looks at 2 csv's of student data to find unique names. The unique
names are returned on a new spreadsheet, with all of their data, and the
duplicates are excluded (though a list of these is printed out). Useful
especially for historical students import. The second csv is compared against
the first, i.e. the "base" is filename1.csv and the comparison is
filename2.csv. The students that do not appear in filename1.csv but are in
filename2.csv will be the ones returned. Assumes no duplicate students.

Requires: 2 csv's, each with a Full Name column

Usage: ./compare_csvs_for_new_students.py {filename1.csv} {filename2.csv}

Returns: spreadsheet of students who appear in filename2.csv, but not in
filename1.csv
"""

import qs
import sys


def main():
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    csv_orig_students = qs.CSV(filename1)
    csv_new_students = qs.CSV(filename2)

    orig_students = []
    new_students = []
    unique_students = []
    duplicate_students = []

    for student in csv_orig_students:
        print student
        student_name = student['Full Name']
        orig_students.append(student_name)
    print orig_students

    for student in csv_new_students:
        student_name = student['Full Name']
        new_students.append(student_name)
    print
    print new_students

    for name in orig_students:
        if name in new_students:
            duplicate_students.append(name)
        else:
            unique_students.append(name)

    print duplicate_students
    print
    print unique_students




if __name__ == ('__main__'):
    main()