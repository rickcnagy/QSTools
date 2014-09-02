#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Extract the first and last names from a "Last, First" Full Name column.

Usage:
    ./separate_first_last {filename.csv} [{overwrite}]

Requires:
    A column entitled "Full Name" where all the names are in "Last, First" or
    "First Last".

Params:
    filename: the filename
    overwrite: whether or not to overwrite the existing file. Defaults to
        False.

Outputs:
    The same CSV, but with "First" and "Last" columns added.
"""

import sys
import qs


def main():
    filename = sys.argv[1]
    overwrite = qs.to_bool(sys.argv[2]) if len(sys.argv) > 1 else False
    csv = qs.CSV(filename)

    csv.cols.insert(csv.cols.index('Full Name') + 1, 'First')
    csv.cols.insert(csv.cols.index('Full Name') + 2, 'Last')
    for row in csv:
        full_name = row['Full Name'].strip()
        split_by_comma = full_name.split(',')
        split_by_space = full_name.split(' ')

        if len(split_by_comma) == 2:
            row['First'] = split_by_comma[1].strip()
            row['Last'] = split_by_comma[0].strip()
        elif len(split_by_space) == 2:
            row['First'] = split_by_space[0].strip()
            row['Last'] = split_by_space[1].strip()
    csv.save("with first last", overwrite=overwrite)


if __name__ == '__main__':
    main()
