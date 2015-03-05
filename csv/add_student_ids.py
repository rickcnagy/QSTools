#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Add a Student ID to each student row based on the First and Last or Full
Name columns.

If ignore_case is true, this will ignore case when matching student names

This doesn't save unless it finds matches for **all students in the csv**.

Usage:
    ./add_student_id {schoolcode} {filename.csv} {opt ignore_case} {opt enrolled_only}

Requires:
    A CSV with "First" and "Last" columns, with an exact name match to the
        provided school database for each student.

Outputs:
    The same CSV, but with a "Student ID" column.
"""

import sys
import qs


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    ignore_case = bool(sys.argv[3]) if len(sys.argv) > 3 else True
    enrolled_only = bool(sys.argv[4]) if len(sys.argv) > 4 else False
    csv_students = qs.CSV(filename)
    q = qs.API(schoolcode)

    if not ('Full Name' in csv_students.cols
            or ('First' in csv_students.cols
            and 'Last' in csv_students.cols)):
        raise ValueError('Full Name or First and Last name columns required.')

    if enrolled_only is True:
        db_students = q.get_students()
    else:
        db_students = q.get_students(
            show_has_left=True,
            show_deleted=True,
            ignore_deleted_duplicates=True)
    db_duplicates = qs.find_dups_in_dict_list(db_students, 'fullName')

    if db_duplicates:
        qs.logger.critical(
            'Student names are not unique in DB, duplicates:',
            db_duplicates)
    else:
        qs.logger.info('Student names are unique.')

    if ignore_case is True:
        for student in db_students:
            student['fullName'] = student['fullName'].lower()
    db_by_name = qs.dict_list_to_dict(db_students, 'fullName')

    student_names_not_matched = set()
    for csv_student in csv_students:
        if 'Full Name' in csv_student:
            csv_full_name = csv_student['Full Name']
        else:
            csv_full_name = '{}, {}'.format(
                csv_student['Last'],
                csv_student['First'])

        csv_original_full_name = csv_full_name
        if ignore_case:
            csv_full_name = csv_full_name.lower()
        db_match = db_by_name.get(csv_full_name)
        if db_match:
            csv_student['Student ID'] = db_match['id']
        else:
            student_names_not_matched.add(csv_original_full_name)

    if student_names_not_matched:
        qs.logger.warning(
            ('{} students in the file were not found in the db'
                ''.format(len(student_names_not_matched))),
            student_names_not_matched)
    else:
        qs.logger.info('All students were matched in the db.')
    csv_students.save(filepath="with student IDs")

if __name__ == '__main__':
    main()
