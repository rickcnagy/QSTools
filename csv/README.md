CSV Scripts
===

####[`add_student_ids.py`](./add_student_ids.py)

Add a Student ID to each student row based on the First and Last or Full
Name columns.

If ignore_case is true, this will ignore case when matching student names

Usage:
    ./add_student_id {filename.csv} {schoolcode} {ignore_case} {enrolled_only}

Requires:
    A CSV with "First" and "Last" columns, with an exact name match to the
        provided school database for each student.

Outputs:
    The same CSV, but with a "Student ID" column.


####[`logs/`](./logs)

####[`separate_first_last.py`](./separate_first_last.py)

Extract the first and last names from a "Last, First" Full Name column.

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
