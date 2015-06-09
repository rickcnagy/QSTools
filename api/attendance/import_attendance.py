#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Import attendance records from a CSV.

Required Columns:
    Student ID
    Teacher ID
    Date
    Status
    Remarks
    Description

Command Line Usage:
    ./import_attendance {filename} {schoolcode}
"""

import sys
import qs


def main():
    qs.logger.config(__file__)
    filename = sys.argv[1]
    schoolcode = sys.argv[2]
    attendance = qs.CSV(filename)
    q = qs.API(schoolcode)

    for row in qs.bar(attendance):
        q.post_attendance(
            row['Student ID'],
            row['Teacher ID'],
            row['Date'],
            row['Status'],
            row['Remarks'],
            row['Description'])

if __name__ == '__main__':
    main()
