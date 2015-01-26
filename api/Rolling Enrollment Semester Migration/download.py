#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Download info from Q1

output contains for each subject:
- all invalid grades (invalid_grades)
- all enrolled students without valid grades (enrolled_no_valid_grades)

This adds all sections, even with nothing to migrate

CLI Usage:
./download.py {schoolcode}
"""

import sys
import qs

schoolcode = sys.argv[1]
CUTOFF_DATE = qs.parse_datestring('2014-9-22')
q = qs.API(schoolcode)


def main():
    qs.logger.config(__file__)
    output = {}

    for section_dict in qs.bar(q.get_sections()):
        section_id = section_dict['id']
        section_output = {}

        valid_grades, invalid_grades = get_valid_and_invalid_grades(section_id)
        section_output['invalid_grades'] = invalid_grades

        all_enrolled = [
            i['smsStudentStubId']
            for i in q.get_section_enrollment(section_id)['students']
        ]

        enrolled_w_valid_grades = [i['studentId'] for i in valid_grades]
        enrolled_no_valid_grades = [
            i for i in all_enrolled
            if i not in enrolled_w_valid_grades
        ]
        section_output['enrolled_no_valid_grades'] = enrolled_no_valid_grades

        output[section_id] = section_output

    qs.write(qs.dumps(output), 'rolling_migration.json')


def get_valid_and_invalid_grades(section_id):
    """returns valid, invalid

    Doesn't look at final grades - valid or not"""
    valid = []
    invalid = []

    grades = q.get_grades(section_id, fields='date')
    if grades:
        grades_of_enrolled_students = filter_for_enrolled_students(grades)
        grades_of_enrolled_students = [
            i for i in grades_of_enrolled_students
            if i['isFinalGrade'] is False
        ]
        for grade in grades_of_enrolled_students:
            fix_grade(grade)
            if is_valid_grade(grade):
                valid.append(grade)
            else:
                invalid.append(grade)
    return valid, invalid


def filter_for_enrolled_students(grades):
    filtered = []
    for grade in grades:
        if is_valid_student(grade['studentId']):
            filtered.append(grade)
    return filtered


def is_valid_student(student_id):
    student = q.get_student(student_id, fields=['hasLeft', 'isExpelled'])
    return student['hasLeft'] is False and student['isExpelled'] is False


def is_valid_grade(grade):
    """Valid = keep in Q1"""
    if not grade['marks']:
        return False
    if grade['marks'] == 'i':
        return False
    if 'date' in grade and qs.parse_datestring(grade['date']) > CUTOFF_DATE:
        return False
    return True


def fix_grade(grade):
    if 'marks' not in grade:
        grade['marks'] = ''

if __name__ == '__main__':
    main()
