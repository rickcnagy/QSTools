"""
Compare Two Semesters' Section Enrollments

This script gets the section enrollments for all students for two semesters,
compares,and outputs a file of descrepancies. Relies on
qs.check_section_enrollment_match()

Usage:
./compare_two_semesters_section_ernrollments.py schoolcode sect1_id sect2_id

Returns: prints list of enrollment discrepancies

"""

import qs
import sys

def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    q = qs.API(schoolcode)
    section1 = sys.argv[2]
    section2 = sys.argv[3]

    discrepancies = q.check_section_enrollment_match(
        section_1_id=section1,
        section_2_id=section2)

    qs.pp({"section1": section1,
           "section2": section2,
           "discrepancies": discrepancies})

if __name__ == '__main__':
    main()