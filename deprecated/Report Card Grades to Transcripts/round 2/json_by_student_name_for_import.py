#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
import json

filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/round 2/Custom Subjects - hand checked.json'
output_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/round 2/Subjects by student name.json'


def main():
    data = json.load(open(filename))
    output = []
    for student_id, subjectDicts in data.iteritems():
        output.append({
            'name': qs.get_student(student_id)['fullName'],
            'subjects': [d for k, d in subjectDicts.iteritems()]
        })
    json.dump(output, open(output_filename, 'w'))


if __name__ == '__main__':
    main()
