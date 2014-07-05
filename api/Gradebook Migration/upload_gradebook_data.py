#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
'''
Upload gradebook data downloaded via download_gradebook_data.py
'''

from tqdm import *
import qs
import api_logging
import data_migration
import os

# skips to section id to resume section id, leave blank to not skip
old_section_start_id = None
has_seen_start_id = False
# won't upload grades for any of these students - should be a list
ignore_student_ids = []

# if not None, will ignore all but valid_sections
valid_sections = ['608040']

# this should generally be false; instead, run check_semesters_match before hand
match_teacher = False


def main():
    data_migration.create_file(prefix='upload', existing_file=True)
    api_logging.config(__file__, log_filename=data_migration.get_filename())
    data_migration.check_before_run()
    assignments = data_migration.load('download')

    posted_assignment_ids = []
    posted_grade_count = 0
    for old_section_id in tqdm(assignments, desc='POST', leave=True):
        if skip(old_section_id): continue

        new_section = qs.match_section_by_id(old_section_id, match_teacher=match_teacher)
        if not new_section or not 'id' in new_section: continue
        new_section_id = new_section['id']

        for original_assignment in assignments[old_section_id]:
            # post assignment to new section
            posted_assignment = qs.post_assignment(new_section_id, original_assignment, critical=True)
            assignment_id = posted_assignment['id']
            posted_assignment_ids.append(original_assignment['assignmentId'])

            # post grades to newly posted assignment
            grades = valid_grades(original_assignment['grades'])
            qs.post_grades(new_section_id, assignment_id, grades, critical=True)
            posted_grade_count += len(grades)

    api_logging.info(
        "Complete. {} errors, {} successeful assignments, {} successful grades."
        "".format(qs.get_error_count(), len(posted_assignment_ids), posted_grade_count),
        {}, cc_print=True)
    data_migration.save(posted_assignment_ids)


# check that the grade has marks and isn't empty
def valid_grades(raw_grades):
    grades = []
    for grade in raw_grades:
        student_id = grade['studentId']
        if ('marks' in grade.keys()
                and student_id not in ignore_student_ids
                and valid_student(student_id)):
            try:
                float(grade['marks'])
                grades.append(grade)
            except(ValueError):
                pass
    return grades


def valid_student(student_id):
    students_by_id = {student['id']: student for student in qs.get_students()}
    if not student_id in students_by_id.keys():
        return False
    elif students_by_id[student_id]['classCode'] == 'N/A':
        return False
    return True


def skip(old_section_id):
    global has_seen_start_id

    if old_section_start_id:
        if not has_seen_start_id:
            if old_section_id == old_section_start_id:
                has_seen_start_id = True
            else:
                return True

    if valid_sections:
        if old_section_id not in valid_sections:
            print old_section_id
            return True

    return False

if __name__ == '__main__':
    main()
