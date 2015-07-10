#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import json
import qs
import csv_tools

input_filepath = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/report cards combined.json'
output_filepath = '/Users/Rick/Dropbox/code/QuickSchools/modules/sa/Students with F in a single section.csv'


def main():
    combined = json.load(open(input_filepath))
    rows = []
    for student, sections in combined.iteritems():
        for section, idents in sections.iteritems():
            s1 = idents.get('s-letter-grade-1')
            s2 = idents.get('s-letter-grade-2')
            if s1 and s2 and ('F' in s1 or 'F' in s2) and s1 != s2:
                rows.append({
                    'Student Name': qs.get_student(student)['fullName'],
                    'Section Name': section,
                    'Semester 1 Grade': s1,
                    'Semester 2 Grade': s2,
                })
    csv_tools.write_csv(rows, output_filepath, keys=['Student Name', 'Section Name', 'Semester 1 Grade', 'Semester 2 Grade'])

if __name__ == '__main__':
    main()
