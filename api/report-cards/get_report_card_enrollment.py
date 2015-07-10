"""
Get Report Card Enrollment

This script takes a CSV of Student IDs and Report Cycle IDs and gets the sections
a student is enrolled in for each report session. Returns a new csv with one row
per student/report cycle/section combination

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
    rc_enrollments = {}
    row_num = 0

    if 'Student ID' not in csv_student_report_cycles.cols:
        raise ValueError("'Student ID' column required.")
    if 'Report Cycle ID' not in csv_student_report_cycles.cols:
        raise ValueError("'Report Cycle ID' column required.")

    for csv_student in csv_student_report_cycles:
        student_id = csv_student['Student ID']
        report_cycle_id = csv_student['Report Cycle ID']

        report_card_data = q.get_report_card(student_id, report_cycle_id)

        print report_card_data


if __name__ == '__main__':
    main()