"""
    Make Multiple Assignments with grade

    Similar to upcoming wrapper function, this script makes an assignment
    and posts a grade to it for a single student. Just in case you want to
    do this via API for some reason.

    Usage:
    ./make-single-assignment-with-grade-py schoolcode filename.csv

    Requires: CSV with the following column headings
        Student ID, Total Pts, Category ID,
        Marks, Grd ID, Section ID

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
import datetime as dt


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
            assign_date = dt.date.today().strftime("%Y-%m-%d")

        section = student_section_record[u'Section ID']
        cat_id = student_section_record[u'Category ID']
        total = student_section_record[u'Total Pts']
        gr_id = student_section_record[u'Grd ID']
        marks = student_section_record[u'Marks']
        student = student_section_record[u'Full Name']
        
        if section not in grades:
            grades[section] = list()
        grades[section].append({student: marks})

        sections[section] = {'cat_id': cat_id,
                             'total': total,
                             'gr_id': gr_id,
                             'assign_date': assign_date,
                             'assign_name': assign_name,
                             'section_id': section}
    for section in sections:
        sections[section]['grades_data'] = grades[section]
        print ""
        print section
        print sections[section]['grades_data']
   
    print ""
    print sections


"""
   # Add grades to assignments
    for student_grades in csv_grades:
        section = student_grades[u'Section ID']
        student = student_grades[u'Student ID']
        marks = student_grades[u'Marks']   
        sections[section]['grades_data'][student] = marks
        grades_data = sections[section]['grades_data']  

    # POST assignment and POST grades to it
    for section in sections:
        print section
        assign_name = sections[section]['assign_name']
        assign_date = sections[section]['assign_date']
        total_possible = sections[section]['total']
        cat_id = sections[section]['cat_id']
        gr_id = sections[section]['gr_id'] 

        for section in sections:
            grades.append({student: grades_data[student]}) 
            print section
        
        print grades
        grades = []

        new_assignment = q.post_assignment(section, assign_name, assign_date,
                                           total_possible, cat_id, gr_id)
        assignment = new_assignment[u'id']
        new_grade = q.post_grades(section_id, assignment,
                                  [sections[section_id]['grades_data']])

        qs.pp({"section": section_id,
               "new assignment id": assignment,
               "grade": sections[section_id]['grades_data'],
               "status": new_grade[u'success']}) """
if __name__ == '__main__':
    main()
