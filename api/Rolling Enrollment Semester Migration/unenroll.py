#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Unenroll enrolled_no_valid_grades students from Q1

Run with either quarter active.

CLI Usage:
./unenroll.py {schoolcode}
"""

import sys
import json
import qs


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    q = qs.API(schoolcode)
    data = json.load(open('rolling_migration.json'))

    for section_id, section_dict in qs.bar(data.iteritems()):
        to_delete = section_dict['enrolled_no_valid_grades']
        if to_delete:
            q.delete_section_enrollments(section_id, to_delete)

if __name__ == '__main__':
    main()
