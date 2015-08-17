#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import json
import numpy

input_filename = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report cards combined.json'
output_filename = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/SA transcript upload data.json'


def main():
    students = json.load(open(input_filename))
    for student, sections in students.iteritems():
        for section_name, identifier_dict in sections.iteritems():
            final_average = average(identifier_dict)
            upload_id = identifier_dict.get('semester 1 id') or identifier_dict.get('semester 2 id')
            identifier_dict['upload id'] = upload_id
            identifier_dict['final average'] = final_average
    json.dump(students, open(output_filename, 'w'), indent=4, sort_keys=True)


def average(identifier_dict):
    try:
        sem1_marks = float(identifier_dict.get('s-marks-1'))
    except (ValueError, TypeError):
        sem1_marks = None
    try:
        sem2_marks = float(identifier_dict.get('s-marks-2'))
    except (ValueError, TypeError):
        sem2_marks = None

    sem1_grade = identifier_dict.get('s-letter-grade-1')
    sem2_grade = identifier_dict.get('s-letter-grade-2')

    avg = 0
    if 'F' in [sem1_grade, sem2_grade]:
        avg = 0
    elif sem1_marks and sem2_marks:
        avg = (float(sem1_marks) + float(sem2_marks)) / 2
        avg = round(avg, 2)
    elif sem1_marks:
        avg = sem1_marks
    elif sem2_marks:
        avg = sem2_marks
    else:
        print 'PROBLEM'
    return str(avg)

if __name__ == '__main__':
    main()
