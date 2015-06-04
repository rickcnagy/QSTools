"""
Enroll in Existing Sections

Imports enrollment from CSV for already created subjects (such as ones imported
through the "Subject (New Style)" importer). Matches by secion code
(abbreviation).

Requires: CSV of enrollment data, semester id

Usage: ./enroll_in_existing_sections.py {school code} {semester} filename.csv

Returns: Nothing - just enrolls students in their sections.

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

    # Get Section Info

    qs.logger.info("Getting section ids...",cc_print=True)
    sections = q.get_sections(semester_id=semester)
    for section in sections:
        section_code = section[u'sectionCode']
        section_id = section[u'id']

        section_enrollments[section_code] = {"sectionCode:": section_code,
                                             "section_id": section_id}
    qs.pp(section_enrollments)



if __name__ == '__main__':
    main()
