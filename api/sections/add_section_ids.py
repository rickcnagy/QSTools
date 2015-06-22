"""
Add Section IDs

Designed to run after add_student_ids.py, which checks for duplicate student
names and gets the students' ids. This script is the next step for a gradebook
import and gets the ids for the sections students are enrolled in. See /samples
for an example csv.

This script doesn't check for duplicates, so you should either know your
database is free of duplicate students, or run this one after running
add_student_ids.py, which checks for this.

Usage:
./add_student_id {schoolcode} {filename.csv}

Requires:
CSV with "Student ID" column, with an exact match to the provided
school database for each student id.

The semester for the subjects you're getting ids for is currently active in the
school's account.

Outputs:
The same CSV with an "Section ID" column
"""

import sys
import qs


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    csv_sections = qs.CSV(filename)
    q = qs.API(schoolcode)
    row_num = 1

    if 'Student ID' in csv_sections.cols:
        qs.logger.info('Retrieving sections from csv & matching with db...',
                       cc_print=True)
        for csv_section_info in qs.bar(csv_sections):
            section_name = csv_section_info['Section Name']
            student = csv_section_info['Student ID']
            row_num = row_num + 1

            section = q.match_section(
                identifier=section_name,
                student_id=student,
                match_name=True)
            section_id = section['id']
            csv_section_info['Section ID'] = section_id
    else:
            sections = {}
            sections_with_id = {}
            row_num = 1

            qs.logger.info('Retrieving section code from csv...',
                           cc_print=True)
            for csv_section_info in csv_sections:
                section_name = csv_section_info[u'Section Name']
                section_code = csv_section_info[u'Section Code']
                row_num = row_num + 1

                if section_code not in sections:
                    sections[section_code] = {'sectionCode': section_code}

            qs.logger.info('GETting matching section ids by section code...',
                           cc_print=True)
            for section_code in sections:
                matched_section = q.match_section(sections[section_code],
                                                  match_code=True)
                section_id = matched_section['id']

                if section_id not in sections_with_id:
                    sections[section_code] = {'section_id': section_id}

            qs.logger.info('Matching section ids to csv section data...',
                           cc_print=True)
            for csv_section_info in csv_sections:
                section_code = csv_section_info['Section Code']
                csv_section_info['Section ID'] = sections[section_code]['section_id']
"""
    filepath = qs.unique_path(csv_sections.filepath, suffix="with section IDs")
    csv_sections.save(filepath)
"""
if __name__ == '__main__':
    main()
