"""
Enroll in Existing Sections

Imports enrollment from CSV for already created subjects (such as ones imported
through the 'Subject (New Style)' importer). Matches by secion code
(abbreviation). Currently handles one semester at a time.

Requires: CSV of enrollment data with subject codes, semester id.
CSV must have the following columns: Student ID, Section Code

Usage: ./enroll_in_existing_sections.py {school code} {semester} filename.csv

Returns: Nothing - just enrolls students in their sections.

## TO DO - MATCH BY SECTION CODE
"""

import qs
import sys


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    semester = sys.argv[2]
    filename = sys.argv[3]
    q = qs.API(schoolcode)
    csv_enrollments = qs.CSV(filename)
    section_enrollments = {}
    student_enrollments = {}

    # Get Section Info

    qs.logger.info('GETting section ids...', cc_print=True)
    sections = q.get_sections(semester_id=semester,
                              active_only=True)
    for section in sections:
        section_code = section[u'sectionCode']
        section_id = section[u'id']
        class_name = section[u'className']

        section_enrollments[section_code] = {'section_code': section_code,
                                             'section_id': section_id,
                                             'class_name': class_name}
    # Setup Enrollment Info

    qs.logger.info('Retrieving enrollment info from csv...', cc_print=True)
    for enrollment in csv_enrollments:
        student_id = enrollment[u'Student ID']
        section_code = enrollment[u'Section Code']

        if section_code not in student_enrollments:
            student_enrollments[section_code] = {'section_code': section_code,
                                                 'students': list()}
        student_enrollments[section_code]['students'].append(student_id)

    qs.logger.info('Preparing for import...', cc_print=True)
    for section in student_enrollments:
        student_enrollments[section]['section_id'] = section_enrollments[section]["section_id"]

    # Do the enrollment import
    qs.logger.info('Importing...', cc_print=True)
    for section in qs.bar(student_enrollments):
        students = student_enrollments[section]['students']
        section_id = student_enrollments[section]['section_id']
        new_enrollment = q.post_section_enrollment(section_id, students)

if __name__ == '__main__':
    main()
