CSV Scripts
===

####[`separate_first_last.py`](./separate_first_last.py)

Extract the first and last names from a "Last, First" Full Name column.

Usage:
    ./separate_first_last {filename.csv}

Requires:
    A column entitled "Full Name" where all the names are in "Last, First"

Outputs:
    The same CSV, but with "First" and "Last" columns added.
