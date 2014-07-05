#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import json
import qs
import csv_tools

filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/INTVLA/INTVLA Grades to Upload.JSON'
enrollment = json.load(open(filename))
csv = csv_tools.CSV()

def main():
    goodcount = 0
    badcount = 0
    for section_id, assignments in enrollment.iteritems():
        section_enrollment = qs.get_section_enrollment(section_id)
        section_enrollment = [i['smsStudentStubId'] for i in section_enrollment]
        csv_enrollment = [i['studentId'] for i in assignments[0]['grades']]
        if not match(section_enrollment, csv_enrollment):
            print 'problem: ' + str(section_id)
            badcount += 1
        else:
            print 'good!'
            goodcount += 1
    print goodcount
    print badcount

def match(one, two):
    if len(one) != len(two): return False
    return len([i for i in one if i not in two]) == 0

if __name__ == '__main__':
    main()
