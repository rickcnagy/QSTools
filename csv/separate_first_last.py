#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""Extract the first and last names from a "Last, First" Full Name column.

Requires:
    A column entitled "Full Name" where all the names are in "Last, First"

Outputs:
    The same CSV, but with "First Name" and "Last Name" columns added.
"""


import qs

FILENAME = '/Users/Rick/Desktop/Student Information - Sheet.csv'
DELIMETER = ','

csv = qs.CSV(FILENAME)

for row in csv:
    full_name = row['Full Name']
    delim_loc = full_name.index(DELIMETER)

    row['First Name'] = full_name[delim_loc + 1:].strip().title()
    row['Last Name'] = full_name[:delim_loc].strip().title()
csv.save()
