#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import qs
import csv_tools

semester_id = '18714'
quarter_num = 2
csv_file = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/CDSG Gradebook Data - Final.csv'


def main():
    csv = csv_tools.CSV(csv_file)
    sections = qs.get_sections(semester_id=semester_id)
    year_name = qs.get_semester(semester_id)['yearName']

    sections = {section['sectionName']: section for section in sections}

    for row in csv:
        if (row['School Year'] == year_name):
            section_id = sections[row['Course Name']]['id']
            row['Q' + str(quarter_num) + ' SectionID'] = section_id

    csv.save()


if __name__ == '__main__':
    main()
