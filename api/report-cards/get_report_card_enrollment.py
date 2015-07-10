"""
Get Report Card Enrollment

This script takes a CSV of Student IDs and Report Cycle IDs and gets the
sections a student is enrolled in for each report session. Returns a new csv
with one row per student/report cycle/section combination. Carries 'Full Name'
and 'Report Cycle' columns into output file, if these are in the original file.

NOTE: Additional columns are not carried through the output file. The only columns
that make it into the output are:
    'Student ID'
    'Full Name' (if in initial csv)
    'Report Cycle ID'
    'Report Cycle' (if initial csv)
    'Section ID'

Requires: CSV with 'Student ID' and 'Report Cycle ID' columns

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
    rc_enrollments = list()

    if 'Student ID' not in csv_student_report_cycles.cols:
        raise ValueError("'Student ID' column required.")
    if 'Report Cycle ID' not in csv_student_report_cycles.cols:
        raise ValueError("'Report Cycle ID' column required.")

    for csv_student in qs.bar(csv_student_report_cycles):
        student_id = csv_student['Student ID']
        report_cycle_id = csv_student['Report Cycle ID']
        if 'Full Name' in csv_student:
            full_name = csv_student['Full Name']
        else:
            full_name = None
        if 'Report Cycle' in csv_student:
            report_cycle = csv_student['Report Cycle']
        else:
            report_cycle = None

        rc_section_data = q.get_report_card(student_id, report_cycle_id)['sectionLevel']

        for section in rc_section_data:
            section_id = section

            if full_name:
                if report_cycle:
                    rc_enrollments.append({'Student ID': student_id,
                                           'Full Name': full_name,
                                           'Report Cycle ID': report_cycle_id,
                                           'Report Cycle': report_cycle,
                                           'Section ID': section_id})
                else:
                    rc_enrollments.append({'Student ID': student_id,
                                           'Full Name': full_name,
                                           'Report Cycle ID': report_cycle_id,
                                           'Section ID': section_id})
            else:
                if report_cycle:
                    rc_enrollments.append({'Student ID': student_id,
                                           'Report Cycle ID': report_cycle_id,
                                           'Report Cycle': report_cycle,
                                           'Section ID': section_id})
                else:
                    rc_enrollments.append({'Student ID': student_id,
                                           'Report Cycle ID': report_cycle_id,
                                           'Section ID': section_id})
    if rc_enrollments:
        qs.logger.info('Report Card section enrollment retrieved', cc_print=True)
        filepath = qs.unique_path(csv_student_report_cycles.filepath)
        qs.write_csv(rc_enrollments, filepath)
    else:
        qs.logger.info('No enrollments found for these students and report cylces', cc_print=True)


if __name__ == '__main__':
    main()