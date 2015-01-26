#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Unenroll all students from all sections in the active semester.

CLI usage:

./delete_all_section_enrollments.py {schoolcode}
"""

import sys
import qs


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    q = qs.API(schoolcode)

    for section_dict in qs.bar(q.get_sections()):
        q.delete_all_section_enrollments_for_section(section_dict['id'])


if __name__ == '__main__':
    main()
