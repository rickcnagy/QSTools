#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Fill in a pivot table CSV such that this:
+------+------+------+------+
| Col1 | Col2 | Col3 | Col4 |
+------+------+------+------+
|    1 |    1 |    1 |    1 |
|      |      |    2 |      |
|      |    2 |    4 |    1 |
|      |      |    5 |      |
+------+------+------+------+

Turns into this:
+------+------+------+------+
| Col1 | Col2 | Col3 | Col4 |
+------+------+------+------+
|    1 |    1 |    1 |    1 |
|    1 |    1 |    2 |      |
|    1 |    2 |    4 |    1 |
|    1 |    2 |    5 |      |
+------+------+------+------+

It stops trying to fill columns once it finds a column that has no empty fields
in it, indicating that blank cells after that column are actually blank data as
opposed to fields to be filled.

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

    cols_to_fill = get_cols_to_fill(csv)

    for row_index in range(0, len(csv)):
        row = csv[row_index]
        for col in cols_to_fill:
            row[col] = resolve_val(row_index, col, csv)
    csv.save()


def get_cols_to_fill(csv):
    to_fill = []
    for col in csv.cols:
        if all(row[col] for row in csv):
            break
        else:
            to_fill.append(col)
    return to_fill


def resolve_val(row_index, col, csv):
    row = csv[row_index]
    if row[col]:
        return row[col]
    elif row_index > 0:
        return resolve_val(row_index - 1, col, csv)
    else:
        return None

if __name__ == '__main__':
    main()
