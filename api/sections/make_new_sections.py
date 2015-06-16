"""
Make New Sections

This script makes sections from identifying data entered in a csv file. It does
not handle any enrollments - just makes the sections in the current active
semester. It does not get section ids (the add_section_ids scripts are good
for this)

Requires: CSV with 'Section Name' 'Section Code' 'Teacher' and 'Class ID'
column headers. 'Credit Hours' is an option

Usage: ./make_new_sections.py {schoolcode} {filename.csv}

Returns: Nothing - just makes the sections in the school account
"""

import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    csv_sections = qs.CSV(filename)
    q = qs.API(schoolcode)
    sections = {}

    qs.logger.info('Retrieving section info from CSV...', cc_print=True)
    for section in csv_sections:
        section_name = section['Section Name']
        section_code = section['Section Code']
        class_id = section['Class ID']
        teacher_id = section['Teacher ID']

        sections[section_code] = {'section_name': section_name,
                                  'section_code': section_code,
                                  'class_id': class_id,
                                  'teacher_id': teacher_id}

        if 'Credit Hours' in section:
            credit_hours = section['Credit Hours']

            sections[section_code]['credit_hours'] = credit_hours

    qs.logger.info('POSTing sections...', cc_print=True)

    new_sections = q.post_sections(sections_dict=sections, print_log=True)

if __name__ == '__main__':
    main()
