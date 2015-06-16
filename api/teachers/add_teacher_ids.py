"""
Add Teacher ID's

GETs teacher ids based on teacher name entered into a csv. Checkes for
duplicates in the csv and database

Requires: Database with Teacher Names, under a 'Teacher' column. The
'ignore_case' param is optional
Usage: ./add_teacher_ids.py {schoolcode} {filename} {ignore_case}

Returns: the same csv, but with teacher ids
"""

import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    ignore_case = bool(sys.argv[3]) if len(sys.argv) > 3 else True
    csv_teachers = qs.CSV(filename)
    q = qs.API(schoolcode)

    if not ('Teacher' in csv_teachers.cols):
        raise ValueError('Teacher column required.')

    db_teachers = q.get_teachers()
    db_duplicates = qs.find_dups_in_dict_list(db_teachers, 'fullName')

    if db_duplicates:
        qs.logger.critical(
            'Teacher names are not unique in DB, duplicates:',
            db_duplicates)
    else:
        qs.logger.info('Teacher names are unique.')

    if ignore_case is True:
        for teacher in db_teachers:
            teacher['fullName'] = teacher['fullName'].lower()
    db_by_name = qs.dict_list_to_dict(db_teachers, 'fullName')

    teacher_names_not_matched = set()
    for csv_teacher in csv_teachers:
        csv_full_name = csv_teacher['Teacher']

        if ignore_case:
            csv_full_name = csv_full_name.lower()

        db_match = db_by_name.get(csv_full_name)
        if db_match:
            csv_teacher['Teacher ID'] = db_match['id']
        else:
            teacher_names_not_matched.add(csv_full_name)

    if teacher_names_not_matched:
        qs.logger.warning(
            ('{} Teachers in the file were not found in the db'
                ''.format(len(teacher_names_not_matched))),
            teacher_names_not_matched)
    else:
        qs.logger.info('All teachers were matched in the db.')
    filepath = qs.unique_path(csv_teachers.filepath, suffix="with teacher IDs")
    csv_teachers.save(filepath)

if __name__ == ('__main__'):
    main()
