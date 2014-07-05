#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Take a CSV with student names and add a student ID column with Student IDs matched by name"""


import qs
import csv_tools

csv_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/INTVLA/INTVLA Grades to Upload.csv'

def main():
    students = qs.get_students()
    student_dir = {}
    for student in students:
        student_dir[student['fullName'].encode('utf8')] = student['id']

    csv = csv_tools.CSV(csv_filename)
    csv.cols.append('Student ID')
    for row in csv:
        row['Student ID'] = student_dir[row['Student Name']]
    csv.save()


if __name__ == '__main__':
    main()
