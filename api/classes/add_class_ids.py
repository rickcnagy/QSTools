"""
Add Class ID

GETs the class ID for a particular class by class name.

Requires: CSV with column of class names

Usage: ./add_class_ids.py {schoolcode} {filename.csv}

Output: same CSV but with a column of class id's
"""

import qs
import sys


def main():
    qs.logger.config(__file__)

    schoolcode = sys.argv[1]
    q = qs.API(schoolcode)
    filename = sys.argv[2]
    csv_classes = qs.CSV(filename)



if __name__ = (__main__):
    main()