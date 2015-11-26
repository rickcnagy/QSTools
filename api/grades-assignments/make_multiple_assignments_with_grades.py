"""
Make Multiple Assignments with grade

This script takes a CSV of grades for particular sections and
makes assignments for that section and posts students' grades
to the assignment.

Usage:
./make-multiple-assignment-with-grade-py schoolcode filename.csv

Requires: CSV with the following column headings
"Student ID", "Total Pts", "Category ID",
"Marks", "Grading Scale ID", "Section ID"

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

    required_columns = ['Section ID', 'Student ID', 'Total Pts', 'Category ID',
        'Marks', 'Grading Scale ID']
    missing_columns = []

    for required_column in required_columns:
        if required_column not in csv_grades.cols:
                missing_columns.append(required_column)

    if missing_columns:
        for missing_column in missing_columns:
            print "Column Missing: {}" . format(missing_column)
        sys.tracebacklimit = 0
        raise ValueError("Columns are missing from CSV. See above for details.")

    # Make dict of students' assignment grades and assignment metadata

    for student_section_record in csv_grades:
        if 'Assignment Name' in student_section_record:
            assign_name = student_section_record[u'Assignment Name']
        else:
            assign_name = 'Grade Import'

        if 'Assignment Date' in student_section_record:
            assign_date = student_section_record['Assignment Date']
        else:
            assign_date = qs.today()

        section = student_section_record['Section ID']
        cat_id = student_section_record['Category ID']
        total = student_section_record['Total Pts']
        grade_scale = student_section_record['Grading Scale ID']
        marks = student_section_record['Marks']
        student = student_section_record['Student ID']

        # List out students' assignment grades
        if section not in grades:
            grades[section] = dict()
        
        if assign_name not in grades[section]:
            grades[section][assign_name] = list()

        grades[section][assign_name].append({'studentId': student, 'marks': marks})

        # List out assignment metadata
        
        print section

        if section not in sections:
            sections[section] = dict()

        sections[section][assign_name] = {'cat_id': cat_id, 'total': total,
            'grade_scale': grade_scale, 'assign_date': assign_date,
            'assign_name': assign_name, 'section_id': section, 'grades_data': []}
    
    for section in sections:
        for assign_name in sections[section]:
            print ""
            print grades[section][assign_name]
            sections[section][assign_name]['grades_data'] = grades[section][assign_name]
            print sections[section][assign_name]['grades_data']

    qs.logger.info(sections, cc_print=True)

    # POST assignment and POST grades to it
    for section in qs.bar(sections):
        for assign_name in sections[section]:
            assign_data = sections[section][assign_name]
            print ""
            print assign_data
            print assign_data['grades_data']
            
            new_grade = q.post_assignment_with_grades(section,
                assign_data['assign_name'], assign_data['assign_date'],
                assign_data['total'], assign_data['cat_id'],
                assign_data['grade_scale'], assign_data['grades_data'])
            


if __name__ == '__main__':
    main()
