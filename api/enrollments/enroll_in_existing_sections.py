"""
Enroll in Existing Sections

Imports enrollment from CSV for already created subjects (such as ones imported
through the 'Subject (New Style)' importer). Matches by section_id.

Requires: CSV of enrollment data with subject codes, semester id.
CSV must have the following columns: "Student ID", "Section Code"

Usage: ./enroll_in_existing_sections.py {school code} {filename.csv}

Returns: Nothing - just enrolls students in their sections.

"""

import qs
import sys


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    q = qs.API(schoolcode)
    csv_enrollments = qs.CSV(filename)
    section_info = {}
    student_enrollments = {}

    # Get Section Info

    if 'Section ID' not in csv_enrollments.cols:
        qs.logger.critical('"Section ID" column required. Current columns: ',
                           csv_enrollments.cols, cc_print=True)

    qs.logger.info('Setting up enrollment info from csv data...', cc_print=True)
    for enrollment in csv_enrollments:
        section_name = enrollment['Section Name']
        section_id = enrollment['Section ID']
        student_id = enrollment['Student ID']
        if 'Section Code' in enrollment:
            section_code = enrollment['Section Code']
        else:
            section_code = enrollment['Section Name']

        if section_id not in student_enrollments:
            student_enrollments[section_id] = list()
        student_enrollments[section_id].append(student_id)

        section_info[section_id] = {'section_name': section_name,
                                    'section_id': section_id,
                                    'section_code': section_code,
                                    'student_ids': student_enrollments[section_id]}

    qs.logger.info('POSTing sections...', cc_print=True)
    for section in qs.bar(section_info):
        section_id = section_info[section]['section_id']
        students = section_info[section]['student_ids']

        new_enrollment = q.post_section_enrollment(section_id, students)

if __name__ == '__main__':
    main()
