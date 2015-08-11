"""
Get Report Card Enrollment

This script takes a CSV of Student IDs gets the sections a student is enrolled
in on their transcript. Returns a new csv with one row per student/section
combination. Carries 'Full Name'into output file, if this was in the original
file.

NOTE: Additional columns are not carried through the output file. The only
columns that make it into the output are:
    'Student ID'
    'Full Name' (if in initial csv)
    'Section ID'

Requires: CSV with 'Student ID' column

Usage: ./get_report_card_enrollment.py {schoolcode} {filename}

Returns: CSV with a 'Section ID' column, with one row per section
"""

import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    q = qs.API(schoolcode)
    csv_student_report_cycles = qs.CSV(filename)
    tr_enrollments = list()

    if 'Student ID' not in csv_student_report_cycles.cols:
        raise ValueError("'Student ID' column required.")

    for csv_student in qs.bar(csv_student_report_cycles):
        student_id = csv_student['Student ID']
        if 'Full Name' in csv_student:
            full_name = csv_student['Full Name']
        else:
            full_name = None

        tr_data = q.get_transcript(student_id)['sectionLevel']

        for section in tr_data:
            section_id = section

            if full_name:
                tr_enrollments.append({'Student ID': student_id,
                                       'Full Name': full_name,
                                       'Section ID': section_id})
            else:
                tr_enrollments.append({'Student ID': student_id,
                                       'Section ID': section_id})

    if tr_enrollments:
        qs.logger.info('Transcript section enrollment retrieved', cc_print=True)
        filepath = qs.unique_path(csv_student_report_cycles.filepath)
        qs.write_csv(tr_enrollments, filepath)
    else:
        qs.logger.info('No enrollments found for these students', cc_print=True)

if __name__ == '__main__':
    main()
