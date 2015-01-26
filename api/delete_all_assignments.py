#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Delete ALL assignments, including final grades, for ALL sections in the
active semester

Be VERY careful with this one.

CLI Usage:
./delete_all_assignments {schoolcode}
"""

import sys
import qs


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    q = qs.API(schoolcode, 'local')

    for section in qs.bar(q.get_sections()):
        section_id = section['id']
        assignments = q.get_assignments(section_id, include_final_grades=True)
        if assignments:
            for assignment in assignments:
                q.delete_assignment(section_id, assignment['id'])


if __name__ == '__main__':
    main()
