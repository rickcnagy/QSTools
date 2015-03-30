#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Fill in a pivot table CSV such that this:
+------+------+------+
| Col1 | Col2 | Col3 |
+------+------+------+
|    1 |    1 |    1 |
|      |      |    2 |
|      |    2 |    4 |
|      |      |    5 |
+------+------+------+

Turns into this:
| Col1 | Col2 | Col3 |
+------+------+------+
|    1 |    1 |    1 |
|    1 |    1 |    2 |
|    1 |    2 |    4 |
|    1 |    2 |    5 |
+------+------+------+

Example input sheet:
examples/fill_in_pivot.sample.csv

CLI Usage:
python fill_in_pivot.py {pivot CSV filename}
"""

import sys
import qs


def main():
    filename = sys.argv[1]
    csv = qs.CSV(filename)

    for row_index in range(0, len(csv)):
        row = csv[row_index]
        for column in row:
            row[column] = resolve_val(row_index, column, csv)
    csv.save()


def resolve_val(row_index, column, csv):
    row = csv[row_index]
    if row[column]:
        return row[column]
    else:
        return resolve_val(row_index - 1, column, csv)

if __name__ == '__main__':
    main()
