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
            s1_grade = idents.get('s-letter-grade-1')
            s1_marks = idents.get('s-marks-1')
            s2_grade = idents.get('s-letter-grade-2')
            s2_marks = idents.get('s-marks-2')
            if (s1_grade and 'F' in s1_grade) or (s2_grade and 'F' in s2_grade): continue

            if s1_grade and not s1_marks:
                print 'S1'
                print student
                print section
                print
                print
            elif s2_grade and not s2_marks:
                print 'S2'
                print student
                print section
                print
                print

if __name__ == '__main__':
    main()
