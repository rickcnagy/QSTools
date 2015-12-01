"""
Add Section IDs

This script gets the section IDs for a set of sections either by student
semester ("Semester ID" col), section code ("Section Code" col) or by
student id ("Student ID" col)

This script doesn't check for duplicate students, so you should either know
your database is free of duplicate students, or run this one after running
add_student_ids.py, which checks for this.

Usage:
./add_student_id {schoolcode} {filename.csv}

Requires:
CSV with "Section Name" columns and "Semester ID", "Section Code" or
"Student ID" columns

The "Student ID" and "Section Code" matches require that the semester you're
getting section id's for is active in the account.

The "Student ID" match assumes the students are already enrolled in the section

The "Semester ID" match assumes that there is only one section with the section
name in each semester

Outputs:
The same CSV with an "Section ID" column
"""

import sys
import qs


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    silent = bool(sys.argv[3]) if len(sys.argv) > 3 else False
    csv_sections = qs.CSV(filename)
    q = qs.API(schoolcode)
    row_num = 1

    if 'Semester ID' in csv_sections.cols:
        qs.logger.info('Matching with db by Semester ID...', cc_print=True)

        for csv_section_info in qs.bar(csv_sections):
            section_name = csv_section_info['Section Name']
            semester_id = csv_section_info['Semester ID']

            if 'Section Code' in csv_sections.cols:
                section_code = csv_section_info['Section Code']
                section = {'sectionCode': section_code}
                matched_section = q.match_section(section, fail_silent=silent, match_code=True,
                    target_semester_id=semester_id)
            else:
                matched_section = q.match_section(identifier=section_name, fail_silent=silent,
                    target_semester_id=semester_id)
            if matched_section is "FALSE":
                section_id = "FALSE"
            else:
                section_id = matched_section['id']
            
            csv_section_info['Section ID'] = section_id

    elif 'Student ID' in csv_sections.cols:
        qs.logger.info('Matching with db by Student ID...', cc_print=True)

        for csv_section_info in qs.bar(csv_sections):
            section_name = csv_section_info['Section Name']
            student = csv_section_info['Student ID']
            row_num += 1

            section = q.match_section(
                identifier=section_name,
                student_id=student,
                match_name=True)
            section_id = section['id']
            csv_section_info['Section ID'] = section_id

    elif 'Section Code' in csv_sections.cols:
        qs.logger.info('Matching with db by Section Code...', cc_print=True)

        sections = {}
        sections_with_id = {}
        row_num = 1

        for csv_section_info in csv_sections:
            section_name = csv_section_info['Section Name']
            section_code = csv_section_info['Section Code']
            row_num += 1

            if section_code not in sections:
                sections[section_code] = {'sectionCode': section_code}

        qs.logger.info('GETting matching section ids by Section Code...',
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

    else:
        qs.logger.critical('"Student ID", "Semester ID", or "Section Code" columns required. Current columns:',
                           csv_sections.cols)

    # Make CSV only if successful
    if 'Section ID' in csv_section_info:
        filepath = qs.unique_path(csv_sections.filepath, suffix="with section IDs")
        csv_sections.save(filepath)

if __name__ == '__main__':
    main()
