#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
'''
Upload gradebook data downloaded via download_gradebook_data.py
'''

from tqdm import *
import qs
import api_logging
import data_migration
import os
import json

# skips to section id to resume section id, leave blank to not skip
old_section_start_id = None
has_seen_start_id = False
# won't upload grades for any of these students - should be a list
ignore_student_ids = []


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    data_migration.create_file(prefix="upload", existing_file=True)
    api_logging.basicConfig(__file__, log_filename=data_migration.get_filename())
    data_migration.check()
    assignments = data_migration.load()

    posted_assignment_ids = []
    posted_grade_count = 0
    for section_id, assignments in tqdm(
            assignments.iteritems(), 
            total=len(assignments),
            desc='POST',
            leave=True):    
        for assignment in assignments:
            # post assignment to section
            posted_assignment = qs.post_assignment(section_id, assignment)
            assignment_id = posted_assignment['id']
            posted_id = (assignment['assignmentId'] 
                if 'assignmentId' in assignment.keys() 
                else assignment_id)
            posted_assignment_ids.append(posted_id or section_id)
        
            # post grades to newly posted assignment
            grades = valid_grades(assignment['grades'])
            qs.post_grades(section_id, assignment_id, grades)
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
        if ('marks' in grade.keys() and valid_student(student_id)):
            try:
                float(grade['marks'])
                grades.append(grade)
            except(ValueError):
                pass
    return grades


def valid_student(student_id):
    students_by_id = {student['id']: student for student in qs.get_students()}
    if student_id not in students_by_id.keys():
        return False
    elif student_id in ignore_student_ids:
        return False
    elif students_by_id[student_id]['classCode'] == 'N/A':
        return False
    return True


def skip(old_section_id):
    global has_seen_start_id

    # don't skip if id is blank
    if not old_section_start_id: return False

    if (not has_seen_start_id) and (old_section_id != old_section_start_id):
        return True
    else:
        return False


if __name__ == '__main__':
    main()
