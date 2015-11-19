"""
Reconcile Section Classes for Student Class

This script determines the class for a student from the classes of their
section enrollments. For each academic year, the number of courses with a
particular class are summed. The (section) class with the greatest number of
sections connected to it is determined to be the student's class.

Requires: CSV with "Student Name", "Class Name" or "Grade", and "Year" columns

Usage: ./reconcile_section_class_for_student_class.py {filename}

Outputs: CSV with Students, reconciled Class, and Year
"""


import qs
import sys


def main():
    qs.logger.config(__file__)

    filename = sys.argv[1]
    csv_student_sections = qs.CSV(filename)
    students = {}

    if 'Student Name' not in csv_student_sections.cols:
        raise ValueError("'Student Name' column required")
    elif not ('Class Name' in csv_student_sections.cols or ('Grade' in csv_student_sections.cols)):
        raise ValueError("'Class Name' or 'Grade' column required.")
    elif 'Year' not in csv_student_sections.cols:
        raise ValueError("'Year' column required.")

    # Make dict of student class info by year and count number of times a course appears

    for record in csv_student_sections:
        student_name = record['Student Name']
        if 'Class Name' in record:
            class_name = record['Class Name']
        else:
            class_name = record['Grade']
        year = record['Year']

        if student_name not in students:
            students[student_name] = dict()
    
        if year not in students[student_name]:
            students[student_name][year] = dict()
      
        if class_name not in students[student_name][year]:
            students[student_name][year][class_name] = 1
        else:
            students[student_name][year][class_name] += 1

    # TO DO: COMPLETE AS NEEDED


if __name__ == '__main__':
    main()