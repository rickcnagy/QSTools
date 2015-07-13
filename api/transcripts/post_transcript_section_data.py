"""
Post Transcript Section Data

This script takes a csv of 'Student ID', 'Section ID', and identifier values
and POSTs the values to a transcript identifier at the section level. The
'from_identifier' is the column/identifier on the csv, the 'post_to_identifer'
is the identifier on the transcript to post the values.

Requires: CSV with 'Student ID', 'Section ID', and identifier values columns

Usage: ./post_transcript_section_data.py {schoolcode} {from_identifier}
            {post_to_identifer} {filename}

Returns: nothing
"""

import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    from_identifier = sys.argv[2]
    to_identifier = sys.argv[3]
    filename = sys.argv[4]
    q = qs.API(schoolcode)
    csv_section_values = qs.CSV(filename)
    sections = dict()
    empty_sections = list()

    if 'Student ID' not in csv_section_values.cols:
        raise ValueError("'Student ID' column required")
    elif 'Section ID' not in csv_section_values.cols:
        raise ValueError("'Section ID' column required")
    elif from_identifier not in csv_section_values.cols:
        raise ValueError("Identifier '{}'column is required" .format(from_identifier))

    qs.logger.info("Retrieving section information and identifier values...", cc_print=True)
    for section in qs.bar(csv_section_values):
        student_id = section['Student ID']
        section_id = section['Section ID']
        identifier_values = section[from_identifier]

        if identifier_values is not None:
            if student_id not in sections:
                sections[student_id] = dict()
            sections[student_id][section_id] = {'values': {to_identifier: identifier_values}}
        else:
            if 'Full Name' in csv_section_values.cols and 'Section Name' in csv_section_values.cols:
                student_name = section['Student Name']
                section_name = section['Section Name']
                empty_sections.append({student_id: section_id, student_name: section_name})
            else:
                empty_sections.append({student_id: section_id})

    qs.logger.info("POSTing data to transcripts' sections...", cc_print=True)
    for student in qs.bar(sections):

        student_id = student
        transcript_data = sections[student]

        q.post_transcript_section_level(student_id, transcript_data)


if __name__ == '__main__':
    main()