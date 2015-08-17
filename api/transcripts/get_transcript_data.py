"""
Get Report Card Data

This script takes a CSV of Student IDs and Section IDs plus a transcript
identifier and returned a csv containing the value of this
identifier for each section on the transcript. Level param sets whether
an identifier is at the "section" level or "transcript".

Requires: CSV with 'Student ID' entered param for
requested identifier

Usage ./get_transcript_data {schoolcode} {server} {level} {identifier} {filename}

Returns: Same CSV, but with transcript identifier a column
"""


import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    server = sys.argv[2]
    identifier = sys.argv[3]
    level = sys.argv[4]
    filename = sys.argv[5]
    q = qs.API(schoolcode, server)
    csv_transcript_data = qs.CSV(filename)
    student_transcript_data = {}

    if 'Student ID' not in csv_transcript_data.cols:
        raise ValueError("'Student ID' column is required.")
    if not (len(sys.argv) == 6):
        raise ValueError("Incorrect number of params. Please review.")
    if ('Section ID' not in csv_transcript_data.cols and level == "section"):
        raise ValueError("'Section ID' column is required.")
    if (level != "transcript" and level != "section"):
        raise ValueError("'Level' param not defined properly. Please chose 'section' or 'transcript'.")

    qs.logger.info('GETting all transcript data for each student enrollment...', cc_print=True)
    for csv_student in qs.bar(csv_transcript_data):
        student_id = csv_student['Student ID']

        if level == "section":
            section_id = csv_student['Section ID']

            transcript_data = q.get_transcript(student_id)['sectionLevel']

            if section_id in transcript_data:
                if identifier in transcript_data[section_id]:
                    csv_student[identifier] = transcript_data[section_id][identifier]
                else:
                    csv_student[identifier] = None
        if level == "transcript":
            transcript_data = q.get_transcript(student_id)['transcriptLevel']
            if identifier in transcript_data:
                csv_student[identifier] = transcript_data[identifier]
            else:
                csv_student[identifier] = None
        else:
            qs.logger.critical('Transcript level param incorrect.')
    
    qs.logger.info('Values retrieved for identifier:', identifier, cc_print=True)
    filepath = qs.unique_path(csv_transcript_data.filepath, suffix="-values")
    csv_transcript_data.save(filepath)

if __name__ == '__main__':
    main()