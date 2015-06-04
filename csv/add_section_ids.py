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

    for csv_section_info in qs.bar(csv_sections):
        section_name = csv_section_info[u'Section Name']
        student = csv_section_info[u'Student ID']
        row_num = row_num + 1

        section = q.match_section(
            identifier=section_name,
            student_id=student,
            match_name=True)
        section_id = section[u'id']
        csv_section_info['Section ID'] = section_id
        qs.logger.info({"row_num": row_num,
                        "section_name": section_name,
                        "student": student,
                        "section_id": section_id}, cc_print=True)

    filepath = qs.unique_path(csv_sections.filepath, suffix="with section IDs")
    csv_sections.save(filepath)

if __name__ == '__main__':
    main()
