#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Download gradebook data for gradebook migration."""

from tqdm import *
from datetime import datetime
import qs
import api_logging
import data_migration

"""set the source semester by id, otherwise it'll use the active semester"""
source_semester = 17900

"""
filters for all assignments in a date range, inclusive of start + end date
format like '2013-10-28'
"""
start_date = None
end_date = None
teacher_id = None
section_id = None
section_class_id = None


def main():
    data_migration.create_file("download")
    api_logging.config(__file__, log_filename=data_migration.get_filename())
    data_migration.check(compare_date=start_date)

    valid_assignments = {}
    grade_download_count = assignment_download_count = 0

    # ========================================
    # = Download assignments in each section =
    # ========================================
    sections = qs.get_sections(semester_id = source_semester, critical=True)
    for section in tqdm(sections, desc='GET', leave=True):
        section_id = section['id']
        if not valid_section(section_id): continue

        # get assignments
        assignments = qs.get_assignments(section_id)
        if not assignments: continue
        assignment_download_count += len(assignments)

        # ======================================
        # = Download grades in each assignment =
        # ======================================
        valid_assignments[section_id] = []
        for assignment in assignments:
            valid = valid_assignment(assignment, section)
            if valid != True:
                api_logging.info("Invalid assignment", assignment)
                continue

            # get grades
            grades = qs.get_grades(section_id, assignment['id'])

            if not grades: continue
            grade_download_count += len(grades)

            # save grade data for upload later
            valid_assignments[section_id].append({
                'name': assignment['name'],
                'date': assignment['date'],
                'totalMarksPossible': assignment['totalMarksPossible'],
                'columnCategoryId': assignment['categoryId'],
                'grades': grades,
                'sectionId': section_id,
                'assignmentId': assignment['id']})


        if not valid_assignments[section_id]:
            del valid_assignments[section_id]

    # ======================================
    # = Output data and complete execution =
    # ======================================
    data_migration.save(valid_assignments)
    api_logging.info(
        "downloaded {} assignments and {} grades from semester {} "
        "between {} and {}, spanning {} sections. {} total errors."
        "".format(
        assignment_download_count, grade_download_count, source_semester,
        start_date, end_date, len(qs.get_sections()), qs.get_error_count()),
        {}, cc_print=True)


def valid_section(test_section_id):
    """
    always require the section to have students enrolled in it
    also, if section_id is defined, then it's only valid if the test_section_id
        matches the section_id defined
    """
    if section_id and section_id != test_section_id:
        return False
    else:
        return len(qs.get_section_enrollment(test_section_id)) > 0


# filter for after compare date and not a formula (which have blank category ID)
def valid_assignment(assignment, section):
    assignment_date = datetime.strptime(assignment['date'], '%Y-%m-%d')
    first_teacher_id = section['teachers'][0]['id']

    if start_date and assignment_date < datetime.strptime(start_date, '%Y-%m-%d'):
        return "before start date"
    elif end_date and assignment_date > datetime.strptime(end_date, '%Y-%m-%d'):
        return "after end date"
    elif not 'categoryId' in assignment.keys():
        return "missing categoryId --> not an actual assignment"
    elif teacher_id and first_teacher_id != teacher_id:
        return "wrong teacher"
    elif section_id and section['id'] != section_id:
        return "wrong section"
    elif section_class_id and section['classId'] != section_class_id:
        return "wrong class"

    return True


if __name__ == '__main__':
    main()
