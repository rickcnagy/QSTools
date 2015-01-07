#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""
DELETE all sections.

For now, requires enrollment to be 0 for all sections - otherwise, QS throws
a soft error.

Usage:
./delete_all_sections {schoolcode} {server}
"""

import sys
import qs


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    server = sys.argv[2]
    q = qs.API(schoolcode, server)

    for section in qs.bar(q.get_sections()):
        q.delete_section(section['id'])


if __name__ == '__main__':
    main()
