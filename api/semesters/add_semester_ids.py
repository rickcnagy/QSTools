"""
Add Semester ID's

Add a Semester ID to each section row based on "Semester" column. This column
must be unique and match the Semester Name in the db exactly.

Usage:
    ./add_semester_id {schoolcode} {filename.csv}

Requires:
    A CSV with "Semester" column, with an exact name match to the
        provided school database for each semester.

Outputs:
    The same CSV, but with a "Semester ID" column.
"""

import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    q = qs.API(schoolcode)
    csv_semesters = qs.CSV(filename)

    # Check CSV for proper columns and verify unique semester names in db

    if not ("Semester" in csv_semesters.cols):
        raise ValueError("'Semester' column required")

    db_semesters = q.get_semesters()
    db_duplicates = qs.find_dups_in_dict_list(db_semesters, "semesterName")

    if db_duplicates:
        qs.logger.critical('Semester names are not unique in DB. Duplicates:',
                           db_duplicates)
    else:
        qs.logger.info('Semester names are unique. Matching...', cc_print=True)

    db_semesters_by_name = qs.dict_list_to_dict(db_semesters, "semesterName")

    # Check for semesters in CSV that are not in db

    semester_names_not_matched = set()

    for csv_semester in csv_semesters:
        csv_semester_name = csv_semester['Semester']

        csv_original_semester_name = csv_semester_name
        db_match = db_semesters_by_name.get(csv_semester_name)

        if db_match:
            csv_semester['Semester ID'] = db_match['id']
        else:
            semester_names_not_matched.add(csv_original_semester_name)
            print 'db_matcn NOT exists'

    # Match semesters if all are matched

    if semester_names_not_matched:
        qs.logger.info('Semester Names do not match DB:',
                       semester_names_not_matched, cc_print=True)
    else:
        qs.logger.info('All semester names matched')
        filepath = qs.unique_path(csv_semesters.filepath)
        csv_semesters.save(filepath)

if __name__ == ('__main__'):
    main()
