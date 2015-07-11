"""
Get Report Card Data

This script takes a CSV of Student IDs, Seciont IDs, and Report Cycle IDs plus
a report card identifier and returned a csv containing the value of this
identifier for each section on the given report card

Requires: CSV with 'Student ID' and 'Report Cycle ID' and entered param for
requested identifier

Usage ./get_report_card_data {schoolcode} {identifier} {filename}

Returns: Same CSV, but with report card identifier a column
"""


import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    identifier = sys.argv[2]
    filename = sys.argv[3]
    q = qs.API(schoolcode)
    csv_report_card_data = qs.CSV(filename)
    student_report_card_data = {}

    if 'Student ID' not in csv_report_card_data.cols:
        raise ValueError("'Student ID' column is required.")
    if 'Report Cycle ID' not in csv_report_card_data.cols:
        raise ValueError("'Report Cycle ID' column is required.")

    qs.logger.info('GETting all report card data for each student enrollment...', cc_print=True)
    for csv_student in qs.bar(csv_report_card_data):
        student_id = csv_student['Student ID']
        section_id = csv_student['Section ID']
        report_cycle_id = csv_student['Report Cycle ID']

        report_card_data = q.get_report_card(student_id, report_cycle_id)['sectionLevel']

        csv_student[identifier] = report_card_data[section_id][identifier]
    
    qs.logger.info('Values retrieved for identifier:', identifier, cc_print=True)
    filepath = qs.unique_path(csv_report_card_data.filepath, suffix="-values")
    csv_report_card_data.save(filepath)




if __name__ == '__main__':
    main()