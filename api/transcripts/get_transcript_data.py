"""
Get Report Card Data

This script takes a CSV of Student IDs and Section IDs plus a transcript
identifier and returned a csv containing the value of this
identifier for each section on the transcript

Requires: CSV with 'Student ID' entered param for
requested identifier

Usage ./get_transcript_data {schoolcode} {server} {identifier} {filename}

Returns: Same CSV, but with transcript identifier a column
"""


import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    server = sys.argv[2]
    identifier = sys.argv[3]
    filename = sys.argv[4]
    q = qs.API(schoolcode, server)
    csv_transcript_data = qs.CSV(filename)
    student_transcript_data = {}

    if 'Student ID' not in csv_transcript_data.cols:
        raise ValueError("'Student ID' column is required.")
    if 'Section ID' not in csv_transcript_data.cols:
        raise ValueError("'Section ID' column is required.")
    if not len(sys.argv) == 5:
        raise ValueError("Missing param. Please review inputs.")

    qs.logger.info('GETting all transcript data for each student enrollment...', cc_print=True)
    for csv_student in qs.bar(csv_transcript_data):
        student_id = csv_student['Student ID']
        section_id = csv_student['Section ID']

        transcript_data = q.get_transcript(student_id)['sectionLevel']

        if section_id in transcript_data:
            if identifier in transcript_data[section_id]:
                csv_student[identifier] = transcript_data[section_id][identifier]
            else:
                csv_student[identifier] = None
    
    qs.logger.info('Values retrieved for identifier:', identifier, cc_print=True)
    filepath = qs.unique_path(csv_transcript_data.filepath, suffix="-values")
    csv_transcript_data.save(filepath)

if __name__ == '__main__':
    main()