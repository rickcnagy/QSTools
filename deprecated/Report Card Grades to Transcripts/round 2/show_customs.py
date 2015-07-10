#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import json
filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/round 2/Custom Subjects.json'


def main():
    data = json.load(open(filename))
    subject_names = []
    for student, subjects in data.iteritems():
        print subjects
        subject_names += [v['subject-name'] for k, v in subjects.iteritems() if k != 'actual subjects']
    print json.dumps(subject_names, indent=4)

if __name__ == '__main__':
    main()
