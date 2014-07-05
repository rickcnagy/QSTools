#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
import csv_tools
import string
import random

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


def rand_string(size=5, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


if __name__ == '__main__':
    main()
