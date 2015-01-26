#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Unenroll enrolled_no_valid_grades students from Q1

Run with either quarter active.
"""

import json
import qs


def main():
    qs.logger.config(__file__)
    q = qs.API('invtla2', 'live')
    downloaded = json.load(open('rolling_migration.json'))

    for section_id, section_dict in qs.bar(downloaded.iteritems()):
        to_delete = section_dict['enrolled_no_valid_grades']
        if to_delete:
            q.delete_section_enrollments(section_id, to_delete)

if __name__ == '__main__':
    main()
