#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Extract the first and last names from a "Last, First" Full Name column.

Usage:
    ./separate_first_last {filename.csv}

Requires:
    A column entitled "Full Name" where all the names are in "Last, First"

Outputs:
    The same CSV, but with "First" and "Last" columns added.
"""

import sys
import qs

DELIMETER = ','


def main():
    filename = sys.argv[1]
    csv = qs.CSV(filename)

    csv.cols.insert(csv.cols.index('Full Name') + 1, 'First')
    csv.cols.insert(csv.cols.index('Full Name') + 2, 'Last')
    for row in csv:
        full_name = row['Full Name']
        if DELIMETER in full_name:
            delim_loc = full_name.index(DELIMETER)

            row['First'] = qs.tc(full_name[delim_loc + 1:].strip())
            row['Last'] = qs.tc(full_name[:delim_loc].strip())
    csv.save()



if __name__ == '__main__':
    main()
