#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Import report card data at the section level.

Combines things so no more than one POST per student.

Uses the current report cycle.

Will soft error if an entry fails (error but not exit).

Takes a CSV with the following format:
+------------+------------+--------------+-------+
| Student ID | Section ID |  Identifier  | Value |
+------------+------------+--------------+-------+
|     252251 |     669067 | marks        | 110   |
|     252251 |     669067 | letter-grade | A++   |
+------------+------------+--------------+-------+


See examples/import_section_level.example.csv for an example import file.

CLI Usage:
python import_section_level.py {schoolcode} {csv_filename}
"""

import sys
import qs


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    filename = sys.argv[2]

    q = qs.API(schoolcode)
    csv = qs.CSV(filename)

    # {student_id: StudentRC}
    student_rcs = {}
    for row in csv:
        student_id = row['Student ID']
        section_id = row['Section ID']
        identifier = row['Identifier']
        value = row['Value']

        if student_id not in student_rcs:
            student_rcs[student_id] = StudentRC()
        rc = student_rcs[student_id]

        rc.add_section_data(section_id, identifier, value)

    report_cycle_id = q.get_active_report_cycle()['id']
    for student_id, rc in student_rcs.iteritems():
        rc_data = rc.full_report_card_data()
        q.post_report_card_section_level(student_id, report_cycle_id, rc_data)


class StudentRC(object):

    def __init__(self):
        # {section_id: {identifier: value}, ...}
        self.data = {}

    def add_section_data(self, section_id, identifier, value):
        if section_id not in self.data:
            self.data[section_id] = {}
        self.data[section_id][identifier] = value

    def full_report_card_data(self):
        rc_data = {}
        for section_id, section_data in self.data.iteritems():
            rc_data[section_id] = {
                'values': section_data
            }
        return rc_data

if __name__ == '__main__':
    main()
