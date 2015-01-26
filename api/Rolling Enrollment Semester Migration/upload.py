#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Upload data into Q2. Run with Q2 active.

- Enroll all the students in Q2 from (enrolled_no_valid_grades)
- Import (invalid_grades) into Q2

Skips sections where there are no students without valid grades, because then
all those students are staying in Q1.
"""

import json
import qs


def main():
    qs.logger.config(__file__)
    q = qs.API('intvla2', 'local')
    downloaded = json.load(open('download.json'))

    for old_section_id, old_section_dict in qs.bar(downloaded.iteritems()):
        new_section = q.match_section(old_section_id)
        new_section_id = new_section['id']
        enrolled_no_valid_grades = old_section_dict['enrolled_no_valid_grades']
        invalid_grades = old_section_dict['invalid_grades']

        if not enrolled_no_valid_grades: continue
        q.post_section_enrollment(new_section_id, enrolled_no_valid_grades)

        grades_by_assignment = {i['assignmentId']: [] for i in invalid_grades}
        for grade in invalid_grades:
            grades_by_assignment[grade['assignmentId']].append(grade)

        for assignment_id, invalid_grades in grades_by_assignment.iteritems():
            old_assignment = q.get_assignment(assignment_id)
            new_assignment = q.post_assignment(
                new_section_id,
                old_assignment['name'],
                old_assignment['date'],
                old_assignment['totalMarksPossible'],
                old_assignment['categoryId'],
                old_assignment['gradingScaleId'])

            q.post_grades(
                new_section_id,
                new_assignment['id'],
                grades)

if __name__ == '__main__':
    main()
