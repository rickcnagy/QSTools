#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

"""
Fills every assignment in every section with fake gradebook data - useful
for creating fake gradebook data for demo schools or support trial schools.
"""

import requests
import qs
from tqdm import *
import random


def main():
    qs.setup()

    sections = qs.get_all_sections()

    # =========================
    # = Loop through sections =
    # =========================
    for i in tqdm(range(0, len(sections)), desc='POST'):
        section_id = sections[i]['id']

        section_enrollments = qs.get_section_enrollments(section_id)
        if not section_enrollments:
            continue

        assignments = qs.get_assignments(section_id)
        if not assignments:
            continue

        # get all ids enrolled in section
        enrolled_ids = []
        for student in section_enrollments:
            enrolled_ids.append(student['smsStudentStubId'])

        # get assignment ids in section
        assignment_ids = []
        for assignment in assignments:
            assignment_ids.append(assignment['id'])

        # =======================================
        # = Loop through assignments in section =
        # =======================================
        for assignment_id in assignment_ids:
            # make dict for posting
            grades_dict = {}
            for student_id in enrolled_ids:
                grades_dict[student_id] = random.randrange(83, 100)

            qs.post_grades(section_id, assignment_id, grades_dict)


if __name__ == '__main__':
    main()
