"""
Make Multiple Assignments with grade

This script takes a CSV of grades for particular sections and
makes an assignment for that section and posts students' grades
to the assignment.

Usage:
./make-single-assignment-with-grade-py schoolcode filename.csv

Requires: CSV with the following column headings
Student ID, Total Pts, Category ID,
Marks, Grading Scale ID, Section ID

Please note the date must be in YYYY-MM-DD format. Also 'Gr ID'
referrs to the grading scale id - *not the letter grade*

Additional columns supported: Name, Date (these are both for
assignments)

By default, if Name nad Date not included, the assignment name will
be set to the name of the CSV and and the assignment date will
be set to the current date (today).

Assumes one grade per student per section

Returns: success message, and if successful, will post a grade
"""
import qs
import sys


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    q = qs.API(schoolcode)
    csv_grades = qs.CSV(filename)
    sections = {}
    grades = {}

    # Make dict of assignment data

    for student_section_record in csv_grades:
        if 'Assignment Name' in student_section_record:
            assign_name = student_section_record[u'Assignment Name']
        else:
            assign_name = 'Grade Import'

        if 'Assignment Date' in student_section_record:
            assign_date = student_section_record[u'Assignment Date']
        else:
            assign_date = qs.today()

        section = student_section_record[u'Section ID']
        cat_id = student_section_record[u'Category ID']
        total = student_section_record[u'Total Pts']
        grade_scale = student_section_record[u'Grading Scale ID']
        marks = student_section_record[u'Marks']
        student = student_section_record[u'Student ID']

        if section not in grades:
            grades[section] = list()
        grades[section].append({'studentId': student, 'marks': marks})

        sections[section] = {'cat_id': cat_id,
                             'total': total,
                             'grade_scale': grade_scale,
                             'assign_date': assign_date,
                             'assign_name': assign_name,
                             'section_id': section}
    for section in sections:
        sections[section]['grades_data'] = grades[section]

    qs.logger.info(sections)

    # POST assignment and POST grades to it
    for section in qs.bar(sections):
        section_data = sections[section]
        new_grade = q.post_assignment_with_grades(section,
                                                  section_data['assign_name'],
                                                  section_data['assign_date'],
                                                  section_data['total'],
                                                  section_data['cat_id'],
                                                  section_data['grade_scale'],
                                                  section_data['grades_data'])

if __name__ == '__main__':
    main()
