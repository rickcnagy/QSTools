#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Import fees for each student from a CSV. Imports 1 fee per row.


The CSV should have the following columns:
- Student ID
- Amount
- Date
- Description

Command line usage:
./import_fees {CSV filename} {schoolcode}
"""

import sys
import qs


def main():
    qs.logger.config(__file__)
    filename = sys.argv[1]
    schoolcode = sys.argv[2]
    fees = qs.CSV(filename)
    q = qs.API(schoolcode)

    for fee in qs.bar(fees):
        q.post_fee(
            fee['Student ID'],
            fee['Amount'],
            fee['Date'],
            fee['Description'])

if __name__ == '__main__':
    main()
