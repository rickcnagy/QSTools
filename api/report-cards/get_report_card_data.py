"""
Get Report Card Data

This script takes a CSV of student names and report cycles and returns a
csv of all the identifiers and values of a student's report card. Identifiers
are columns, rows are student/report cycles

Requires: CSV with 'Student ID' and 'Report Cycle ID'

Usage ./get_report_card_data {schoolcode} {filename}

Returns: Same CSV, but with report card identifiers as columns
"""


import qs
import sys

def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    q = qs.API(schoolcode)
    csv_report_card_data = qs.CSV(filename)

    if 'Student ID' not in csv_report_card_data:
        raise ValueError("'Student Name' column is required.")
    if 'Report Cycle ID' not in csv_report_card_data:
        raise ValueError("'Report Cycle ID' column is required.")

    for csv_student in csv_report_card_data:
        student_id = csv_student['Student ID']
        report_cycle_id = csv_student['Report Cycle ID']

        report_card_data = q.get_report_card_data(student_id=student_id,
                                                  report_cycle_id=report_cycle_id)

        

if __name__ == '__main__':
    main()