#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import csv_tools
import qs
csv = csv_tools.CSV('/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/CDSG Gradebook Data - Final.csv')


def main():
    q1_sections = {}
    ret = ''
    filtered_rows = [i for i in csv.rows if i['School Year'] == '2009/2010']
    for row in filtered_rows:
        section_id = row['Q2 SectionID']
        if not section_id in q1_sections:
            q1_sections[section_id] = 0
        q1_sections[section_id] += 1

    for section_id, count in q1_sections.iteritems():
        enrollment = len(qs.get_section_enrollment(section_id))
        if enrollment != count:
            ret += '{}: should be {}, is {}\n'.format(section_id, count, enrollment)
    print ret


if __name__ == '__main__':
    main()
