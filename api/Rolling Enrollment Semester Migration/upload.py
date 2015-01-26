#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Upload data into Q2. Run with Q2 active.

- Enroll all the students in Q2 from (enrolled_no_valid_grades)
- Import (invalid_grades) into Q2

Skips sections where there are no students without valid grades, because then
all those students are staying in Q1.

CLI Usage:
./upload.py {schoolcode}
"""

import sys
import json
import qs


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    q = qs.API(schoolcode, 'local')
    data = json.load(open('rolling_migration.json'))

    for old_section_id, old_section_dict in qs.bar(data.iteritems()):
        new_section = q.match_section(old_section_id)
        new_section_id = new_section['id']
        enrolled_no_valid_grades = old_section_dict['enrolled_no_valid_grades']
        invalid_grades = old_section_dict['invalid_grades']

        if not enrolled_no_valid_grades: continue

        q.post_section_enrollment(new_section_id, enrolled_no_valid_grades)

        invalid_by_assignment = {i['assignmentId']: [] for i in invalid_grades}
        for grade in invalid_grades:
            if grade['isFinalGrade'] is False:
                invalid_by_assignment[grade['assignmentId']].append(grade)

        for assignment_id, grades in invalid_by_assignment.iteritems():
            old_assignment = q.get_assignment(assignment_id)
            new_assignment = q.post_assignment(
                new_section_id,
                old_assignment.get('name'),
                old_assignment.get('date'),
                old_assignment.get('totalMarksPossible'),
                old_assignment.get('categoryId'),
                old_assignment.get('gradingScaleId'))

            grades_to_upload = []
            for grade in grades:
                student_id = grade['studentId']
                if student_id in enrolled_no_valid_grades:
                    grades_to_upload.append(grade)
                else:
                    warning = ("student {} has some, but not all valid grades "
                        "for section {}").format(student_id, old_section_id)
                    qs.logger.warning(warning)

            q.post_grades(
                new_section_id,
                new_assignment['id'],
                grades_to_upload)

if __name__ == '__main__':
    main()
