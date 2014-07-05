#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
import json

output_file = 'term 2 enrollment.json'


def main():
    output = {}
    for student in qs.get_students(fields='smsClassSubjectSetPrettyList'):
        subjects = student['smsClassSubjectSetPrettyList'].split('\n')
        if subjects != ['']:        
            output[student['id']] = {
                'studentName': student['fullName'],
                'subjects': subjects,
            }
    json.dump(output, open(output_file, 'w'), indent=4)


if __name__ == '__main__':
    main()
