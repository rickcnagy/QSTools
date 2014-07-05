#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
import json

input_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/round 2/Custom Subjects - hand checked.json'
output_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/round 2/Subjects to add.json'


def main():
    by_id = json.load(open(input_filename))
    by_name = []
    for student_id, subjects in by_id.iteritems():
        by_name.append({
            'name': qs.get_student(student_id)['fullName'],
            'subjectCount': len(subjects)
        })
    json.dump(by_name, open(output_filename, 'w'))

if __name__ == '__main__':
    main()
