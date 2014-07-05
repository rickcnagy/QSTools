#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import json

data = json.load(open('/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/SA subjects to hide.json'))

for student in data:
    student['Subjects'] = student['Subjects'].split(' | ')

json.dump(data, open('/Users/Rick/Dropbox/code/QuickSchools/QS API/Report Card Grades to Transcripts/SA subjects to hide 1.json', 'w'))
