#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""
Import Fees

Import fees for each student from a CSV. Imports 1 fee per row. Negative
fees are counted as payments, postive fees are counted as charges. Category
ID is an option param (column 'Category ID').


The CSV should have the following columns:
- Student ID
- Amount
- Date
- Description


Command line usage:
./import_fees {schoolcode} {CSV filename}
"""

import sys
import qs


def main():
    qs.logger.config(__file__)
    schoolcode = sys.argv[1]
    filename = sys.argv[2]
    q = qs.API(schoolcode)
    fees = qs.CSV(filename)

    for fee in qs.bar(fees):
        q.post_fee(
            fee['Student ID'],
            fee['Category ID'],
            fee['Amount'],
            fee['Date'],
            fee['Description'])

if __name__ == '__main__':
    main()
