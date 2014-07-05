#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import csv_tools
import json

in_final_id = '42976'
not_in_final_id = '42977'

input_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/INTVLA/INTVLA Grades to Upload.csv'
outut_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/INTVLA/INTVLA Grades to Upload modified.JSON'
csv = csv_tools.CSV(input_filename)


def main():
    # {sectionId: {[]} (all quarters)
    sections = {r['New Section ID']: [] for r in csv}
    for row in csv:
        sections[row['New Section ID']].append(row)
    output = {}
    for section_id, rows in sections.iteritems():
        output[section_id] = [Assignment("Final Grade", section_id, rows, True)]
    output = {k: [i.get_data() for i in v] for k, v in output.iteritems()}
    json.dump(output, open(outut_filename, 'w'), indent=4)


def grade2marks(grade):
    guide = {
        'A': 95,
        'B': 85,
        'C': 75,
        'D': 65,
        'F': 55,
        'I': None,
        ' ': None,
        'p': None,
    }
    return guide[grade[:1]]


class Assignment(object):

    def __init__(self, name, section_id, rows, in_final):
        self.name = name
        self.section_id = section_id
        self.rows = rows
        self.column_id = in_final_id if in_final else not_in_final_id
        self.grades = []
        self.add_grades()

    def add_grades(self):
        for row in self.rows:
            self.grades.append({
                "studentId": row['Student ID'],
                "marks": grade2marks(row['Letter Grade']),
            })

    def get_data(self):
        return {
            "name": self.name,
            "sectionId": self.section_id,
            "grades": self.grades,
            "date": "2014-06-1",
            "totalMarksPossible": 100,
        }

if __name__ == '__main__':
    main()
