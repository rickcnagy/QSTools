#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import csv_tools
import json

in_final_id = '42976'
not_in_final_id = '42977'

input_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/Changes/CDSG Gradebook Data - Final.csv'
outut_filename = '/Users/Rick/Dropbox/code/QuickSchools/QS API/Gradebook Import/CDSG Gradebook Data for input.JSON'

csv = csv_tools.CSV(input_filename)


def main():
    # {sectionId: {quarter: 1, students: [student 1, student 2]}} (all quarters)
    sections = {}
    for row in csv:
        for quarter in range(1, 5):
            section_id = row['Q{} SectionID'.format(quarter)]
            if not section_id: continue
            if section_id not in sections:
                sections[section_id] = {'quarter': quarter, 'rows': []}
            sections[section_id]['rows'].append(row)

    # {sectionId: [{name: Q1 Final Grade, grades: "json"}, {name: Sem1 Final Grade, grades: "json"}]}
    # [Assignment, Assignment, etc]
    output = {}
    for section_id, section in sections.iteritems():
        rows = section['rows']
        q = section['quarter']
        output[section_id] = []
        if q in [1, 2]:
            output[section_id].append(Assignment('Semester 1', section_id, rows, True))
        else:
            output[section_id].append(Assignment('Semester 2', section_id, rows, True))
        if q == 1:
            output[section_id].append(Assignment('First Term', section_id, rows, False))
        elif q == 2:
            output[section_id].append(Assignment('Second Term', section_id, rows, False))
            output[section_id].append(Assignment('Final Exam 1', section_id, rows, False))
        elif q == 3:
            output[section_id].append(Assignment('Third Term', section_id, rows, False))
        elif q == 4:
            output[section_id].append(Assignment('Fourth Term', section_id, rows, False))
            output[section_id].append(Assignment('Final Exam 1', section_id, rows, False))
    output = {k: [i.get_data() for i in v] for k, v in output.iteritems()}
    json.dump(output, open(outut_filename, 'w'), indent=4)

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
                "marks": row[self.name],
            })

    def get_data(self):
        return {
            "name": self.name,
            "sectionId": self.section_id,
            "columnCategoryId": self.column_id,
            "grades": self.grades,
            "date": "2014-06-06",
            "totalMarksPossible": 100,
        }

if __name__ == '__main__':
    main()
