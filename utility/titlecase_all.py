#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Titlecase all cells (except for headers) in a CSV

CLI Usage:
python titlecase_all.py filepath
"""

import sys
import os
import qs


def main():
    filepath = os.path.expanduser(sys.argv[1])
    csv = qs.CSV(filepath)

    for row in csv:
        for key, value in row.iteritems():
            row[key] = qs.tc(value)

    csv.save()

if __name__ == '__main__':
    main()
