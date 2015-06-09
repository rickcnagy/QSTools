""" Converts spreadsheets for import for the Student-Subject Set/Band Importer.
Designed to handle spreadsheets in a form where each enrollment is on a single
line. 

Spreadsheet column names : Student Name     Subject Name

Essentially, this works a lot like transposing the spreadsheet would look,
except it's still a vertical table, but with one row per student, and subjects
separated by columns. Requires student names in format "Last, First" or 
"First Last". Also, spreadsheet must be sorted by student name alphabetically."""

import sys # what does this do
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
            ignore_unenrolled_duplicates=True)
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
    csv_students.save("with student IDs")

if __name__ == '__main__':
    main()